import subprocess

import json
import argparse
from pytube import YouTube

from urllib.parse import urlparse, parse_qs

from app.preprocessing.gemini_video import Video

def gemini_video_summary(video_url): 
    response = Video.call_gemini(video_url)
    return response



def gemini_output_to_audio(yt_id, save_path="./app/static/app/audios"):

    # videoPath = "https://www.youtube.com/watch?v=" + videoId
    # videoPath = "https://www.youtube.com/watch?v=-bzWSJG93P8"

    video_path = "https://www.youtube.com/watch?v=" + yt_id
    print(video_path)

    #TODO: modify api to get multiple video links
    # keep checking, until we get valid video link

    try:
        yt = YouTube(
        video_path,
        use_oauth=True,
        allow_oauth_cache=True
        )
        stream_query = yt.streams.filter(only_audio=True)
        stream_data = yt.streams.get_by_itag(stream_query[0].itag)

        try:
            audio_path = stream_data.download(output_path=save_path, filename = 'audio_'+yt_id+'.mp3')
            print(f"Successfully downloaded at :{audio_path}")
        except:
            print("Couldn't download audio file.")
    except:
        print("Some error occured. Use non age-restricted videos please.")


def remove_audio_from_video():

    '''
    -i input.mp4: This specifies the input file. Replace input.mp4 with the path to your video file.
    -c:v copy: This option copies the video codec as is, without re-encoding the video stream.
    -an: This option removes the audio stream from the video.
    output.mp4: This is the name of the output file. The resulting video will have no audio.
    '''

    command = "ffmpeg -i ./app/static/app/videos/input.mp4 -c:v copy -an ./app/static/app/videos/output.mp4"
    output = subprocess.run(
          command,
        shell=True,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    print("Command output:", output.stdout)


def merge_audio_files():
    """
    -i audio1.mp3 -i audio2.mp3: Specifies the input audio files.
    [0:a]afade=t=out:st=10:d=5[aud1]: Applies a fade out to the first audio at 10 seconds lasting 5 seconds.
    [1:a]afade=t=in:st=0:d=5[aud2]: Applies a fade in to the second audio at the start lasting 5 seconds.
    [aud1][aud2]concat=n=2:v=0:a=1[audio]: Concatenates the two audio streams into one.
    output_audio.mp3: The resulting audio file with a smooth transition.
    """

    command = "ffmpeg -i ./app/static/app/audios/audio1.mp3 -i ./app/static/app/audios/audio2.mp3 -filter_complex '[0:a]afade=t=out:st=10:d=5[aud1]; [1:a]afade=t=in:st=0:d=5[aud2]; [aud1][aud2]concat=n=2:v=0:a=1[audio]' -map '[audio]' ./app/static/app/audios/output_audio.mp3"
    output = subprocess.run(
        command,
        shell=True,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    print("Command output:", output.stdout)

    # os.system("ffmpeg -i audio1.mp3 -i audio2.mp3 -filter_complex '[0:a]afade=t=out:st=10:d=5[aud1]; [1:a]afade=t=in:st=0:d=5[aud2]; [aud1][aud2]concat=n=2:v=0:a=1[audio]' -map '[audio]' output_audio.mp3")

    return None


def merge_audio_video():
    """-i video.mp4: Input video file.
    -itsoffset 00:00:05: Starts the audio file 5 seconds into the video. Adjust 00:00:05 to your desired start time.
    -i audio.mp3: Input audio file.
    -map 0:v: Maps the video stream from the first input (video).
    -map 1:a: Maps the audio stream from the second input (audio).
    -c:v copy: Copies the video codec from the original.
    -c:a aac: Encodes the audio to AAC.
    output.mp4: The output file name."""

    command = "ffmpeg -i ./app/static/app/videos/video.mp4 -itsoffset 00:00:05 -i ./app/static/app/audios/output_audio.mp3 -map 0:v -map 1:a -c:v copy -c:a aac -strict experimental ./app/static/app/videos/output.mp4"
    output = subprocess.run(
        command,
        shell=True,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    print("Command output:", output.stdout)

    # os.system("ffmpeg -i video.mp4 -itsoffset 00:00:05 -i audio.mp3 -map 0:v -map 1:a -c:v copy -c:a aac -strict experimental output.mp4")

    return None
