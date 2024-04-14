import os

import dotenv  # <- New
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from VibeSync import settings

import requests
import logging
from .models import YouTubeVideo
from utils import gemini_output_to_audio, gemini_video_summary

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
                fs = FileSystemStorage(location=os.path.join(settings.BASE_DIR, 'app/static/app/videos'))
                # filename = fs.save(settings.MEDIA_ROOT \ video_file.name, video_file)
                # if file exists, delete it
                if os.path.exists(os.path.join(settings.BASE_DIR, 'app/static/app/videos', video_file.name)):
                    os.remove(os.path.join(settings.BASE_DIR, 'app/static/app/videos', video_file.name))

                filename = fs.save(video_file.name, video_file)
                uploaded_file_url = fs.url(filename)
                return JsonResponse({'message': 'Success', 'fileUrl': uploaded_file_url}, status=200)
            else:
                return JsonResponse({'message': 'No file provided'}, status=400)

        elif request_type == "gemini":
            # gemini integration
            file_url = request.POST.get('file_url', '')
            if file_url != '':
                video_path = os.path.join(settings.BASE_DIR, f'app/static/app/videos{file_url}')
                gemini_response = gemini_video_summary(video_path)
                return JsonResponse({'message': 'Success', 'text': gemini_response}, status=200)
            else:
                return JsonResponse({'message': 'File not found in server'}, status=400)



    return render(request, 'app/index.html')

def get_youtube_link(request, search_query: str):
    video, created = YouTubeVideo.objects.get_or_create(search_query=search_query)
    if not created:
        return JsonResponse({"video_link": video.video_link})
    else:
        base_url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "q": search_query,
            "type": "video",
            "key": YOUTUBE_API_KEY,
        }
        response = requests.get(base_url, params=params)
        data = response.json()
        if data["items"]:
            video_id = data["items"][0]["id"]["videoId"]
            video_link = f"https://www.youtube.com/watch?v={video_id}"
            video.video_link = video_link
            video.save()
            return JsonResponse({"video_link": video_link})
        else:
            return JsonResponse({"error": "No results found"}, status=404)


def get_yt_audio(request, yt_id: str):
    save_path = "./app/static/app/audios"
    gemini_output_to_audio(yt_id, save_path)
    return HttpResponse("Audio extracted successfully!", status=200)