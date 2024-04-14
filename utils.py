import os
import argparse
import json
import subprocess

from pytube import YouTube

from app.preprocessing.gemini_video import Video

from app.constants import SYSTEM_INSTRUCTION
import ffmpeg



output_addr = "app/static/app/output/"
video_addr = "app/static/app/videos/"

def gemini_video_summary(video_url):
    # get system config from system config settings.py
    video = Video(system_instruction=SYSTEM_INSTRUCTION)
    print(video_url)
    response = video.call_gemini(video_url)
    return response


def gemini_output_to_audio(yt_id, save_path="./app/static/app/audios"):

    # videoPath = "https://www.youtube.com/watch?v=" + videoId
    # videoPath = "https://www.youtube.com/watch?v=-bzWSJG93P8"

    video_path = "https://www.youtube.com/watch?v=" + yt_id
    print(video_path)

    # TODO: modify api to get multiple video links
    # keep checking, until we get valid video link

    try:
        yt = YouTube(video_path, use_oauth=True, allow_oauth_cache=True)
        stream_query = yt.streams.filter(only_audio=True)
        stream_data = yt.streams.get_by_itag(stream_query[0].itag)

        try:
            audio_path = stream_data.download(
                output_path=save_path, filename="audio_" + yt_id + ".mp3"
            )
            print(f"Successfully downloaded at :{audio_path}")
        except:
            print("Couldn't download audio file.")
    except:
        print("Some error occured. Use non age-restricted videos please.")


def process_and_concatenate_audios(time_audio_dict ):
    """
    Crop each audio file according to the specified time steps and concatenate them.

    Args:
    time_audio_dict (dict): A dictionary with keys as time ranges in 'start-end' format (seconds)
                            and values as paths to audio files.
    output_file (str): Path to the output file to store the concatenated audio.
    """
    # Prepare a list for storing individual audio segments
    segments = []

    def time_to_secs(time_str):
        m, s = map(int, time_str.split(':'))
        return m * 60 + s

    cross_fade_duration = 3

    previous_end_time = time_to_secs('00:00')
  
    # Process each item in the dictionary
    for time_range, audio_path in time_audio_dict.items():
        print(f'Processing {audio_path} for time range {time_range}')
        start_time, end_time = map(time_to_secs, time_range.split(' - '))
        
        # Load the audio file and trim it according to the specified time range
        audio_segment = ffmpeg.input(audio_path).audio.filter('atrim', start=0, end=end_time-previous_end_time)
        previous_end_time = end_time
        # Reset PTS to ensure correct concatenation
        # audio_segment = audio_segment.filter('aresample','100')
        audio_segment = audio_segment.filter('asetpts', 'PTS-STARTPTS')
        segments.append(audio_segment)

    # # Concatenate all audio segments
    # concatenated = ffmpeg.concat(*segments, v=0, a=1, unsafe=True)  # 'unsafe' is often required for different input streams
    # Initialize the first segment
    concatenated = segments[0]

    # Apply cross-fade with the next segments
    for next_segment in segments[1:]:
        concatenated = ffmpeg.filter([concatenated, next_segment], 'acrossfade', d=cross_fade_duration)


    # Output the final concatenated audio to the specified file

    output_fk = os.path.join(output_addr, 'output.mp3')
    if os.path.exists(output_fk):
        os.remove(output_fk)
    ffmpeg.output(concatenated, output_fk).run()

    return None

def merge_audio_video():
    video_file = os.path.join(video_addr, 'video.mp4')
    save_path = os.path.join(video_addr, 'video_output.mp4')
    if os.path.exists(save_path):
        os.remove(save_path)
    audio_file = os.path.join(output_addr, 'output.mp3')
    video_filename = video_file.split('.')[0]
    probe = ffmpeg.probe(audio_file)
    audio_duration = int(float(probe['format']['duration']))

    probe_video = ffmpeg.probe(video_file)
    video_duration = int(float(probe_video['format']['duration']))
    try:
        assert audio_duration==video_duration
    except AssertionError as msg:
        print(msg)

    input_video = ffmpeg.input(video_file)
    input_audio = ffmpeg.input(audio_file)
    
    # Merge the audio and video
    ffmpeg.concat(input_video, input_audio, v=1, a=1).output(save_path).run() 
    return None
