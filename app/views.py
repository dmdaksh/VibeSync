import os
import json
import dotenv  # <- New
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from VibeSync import settings

import re

import requests
import logging
from .models import YouTubeVideo
from utils import gemini_output_to_audio, gemini_video_summary, process_and_concatenate_audios, merge_audio_video

logger = logging.getLogger(__name__)
# Add .env variables anywhere before SECRET_KEY
dotenv_file = os.path.join(".", ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

# UPDATE secret key
YOUTUBE_API_KEY = os.environ["YOUTUBE_API_KEY"]  # Instead of your actual secret key


def index(request):
    if request.method == "POST":
        request_type = request.POST.get('requestType', '')
        if request_type == "upload":
            video_file = request.FILES.get('video', None)
            if video_file:
                # Define the directory and filename
                directory = os.path.join(settings.BASE_DIR, 'app/static/app/videos')
                filename = 'video.mp4'  # Always use 'video.mp4' as the filename

                fs = FileSystemStorage(location=directory)
                
                # Check if 'video.mp4' exists, delete if it does
                file_path = os.path.join(directory, filename)
                if os.path.exists(file_path):
                    os.remove(file_path)

                # Save the new file
                fs.save(filename, video_file)
                uploaded_file_url = fs.url(filename)
                return JsonResponse({'message': 'Video successfully uploaded', 'fileUrl': uploaded_file_url}, status=200)
            else:
                return JsonResponse({'message': 'No file provided'}, status=400)

        elif request_type == "gemini":
            # gemini integration
            file_url = request.POST.get('file_url', '')
            if file_url != '':
                video_path = os.path.join(settings.BASE_DIR, f'app/static/app/videos{file_url}')
                gemini_response = gemini_video_summary(video_path)
                # print(type(gemini_response))
                json_str = gemini_response.replace("```json", "").replace("```", "")
                # json_str = re.search(r'\[(?:[^[\]]*|(?R))*\]', gemini_response)
                # if json_str:
                #     json_str = json_str.group(0)
                # else:
                #     return JsonResponse({'message': 'Error in processing gemini response'}, status=400)
                print('\n\n')
                print(json_str)
                print('\n\n')
                gemini_json = json.loads(json_str)
                return JsonResponse({'message': 'Success', 'gemini_json': gemini_json}, status=200)
            else:
                return JsonResponse({'message': 'File not found in server'}, status=400)
            
        # elif request_type == "displayOutput":
        #     pass
            # save to db

    return render(request, 'app/index.html')

def get_youtube_link(request):
    youtube_urls = {}
    # song_timestamp_json = json.loads(search_json)
    if request.method == "POST":
        payload = request.POST.get('gemini_response', '')
        print(payload)
        song_timestamp_json = json.loads(payload)
        for entry in song_timestamp_json:
            time_interval = entry['time_interval']
            song_details = entry['song_options'][0]['song_name'] + " " + entry['song_options'][1]['song_artist']
            base_url = "https://www.googleapis.com/youtube/v3/search"
            params = {
                "part": "snippet",
                "q": song_details,
                "type": "video",
                "key": YOUTUBE_API_KEY,
            }
            response = requests.get(base_url, params=params)
            data = response.json()
            if data["items"]:
                video_id = data["items"][0]["id"]["videoId"]
                video_link = f"https://www.youtube.com/watch?v={video_id}"
                youtube_urls[time_interval] = video_link
            else:
                # youtube_urls.append("No results found")
                youtube_urls[time_interval] = "No results found"
        
        # youtube_urls = json.dumps(youtube_urls)
        # print(youtube_urls)
        # return JsonResponse({"youtube_urls": youtube_urls})


        save_path = "./app/static/app/audios"
        # gemini_output_to_audio(yt_id, save_path)

        timestamp_video = {}

        # remove everything inside /app/static/app/audios
        for filename in os.listdir(save_path):
            file_path = os.path.join(save_path, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(f"Error: {e}")

        for key, value in youtube_urls.items():
            yt_id = value.split('=')[-1]
            gemini_output_to_audio(yt_id, save_path)
            # timestamp_video[key] = f"audio_{yt_id}.mp3"
            timestamp_video[key] = os.path.join(save_path, f"audio_{yt_id}.mp3")
        
        

        process_and_concatenate_audios(timestamp_video)

        output_file_path = merge_audio_video()
        
        return JsonResponse({'message': 'Success'}, status=200)