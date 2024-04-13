import subprocess
def merge_audio_files():
    """
    -i audio1.mp3 -i audio2.mp3: Specifies the input audio files.
    [0:a]afade=t=out:st=10:d=5[aud1]: Applies a fade out to the first audio at 10 seconds lasting 5 seconds.
    [1:a]afade=t=in:st=0:d=5[aud2]: Applies a fade in to the second audio at the start lasting 5 seconds.
    [aud1][aud2]concat=n=2:v=0:a=1[audio]: Concatenates the two audio streams into one.
    output_audio.mp3: The resulting audio file with a smooth transition.
    """

    command = "ffmpeg -i audio1.mp3 -i audio2.mp3 -filter_complex '[0:a]afade=t=out:st=10:d=5[aud1]; [1:a]afade=t=in:st=0:d=5[aud2]; [aud1][aud2]concat=n=2:v=0:a=1[audio]' -map '[audio]' output_audio.mp3"
    output = subprocess.run(command, shell=True, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("Command output:", output.stdout)

    # os.system("ffmpeg -i audio1.mp3 -i audio2.mp3 -filter_complex '[0:a]afade=t=out:st=10:d=5[aud1]; [1:a]afade=t=in:st=0:d=5[aud2]; [aud1][aud2]concat=n=2:v=0:a=1[audio]' -map '[audio]' output_audio.mp3")

    return None

def merge_audio_video():
    '''-i video.mp4: Input video file.
    -itsoffset 00:00:05: Starts the audio file 5 seconds into the video. Adjust 00:00:05 to your desired start time.
    -i audio.mp3: Input audio file.
    -map 0:v: Maps the video stream from the first input (video).
    -map 1:a: Maps the audio stream from the second input (audio).
    -c:v copy: Copies the video codec from the original.
    -c:a aac: Encodes the audio to AAC.
    output.mp4: The output file name. '''

    command = "ffmpeg -i video.mp4 -itsoffset 00:00:05 -i audio.mp3 -map 0:v -map 1:a -c:v copy -c:a aac -strict experimental output.mp4"
    output = subprocess.run(command, shell=True, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print("Command output:", output.stdout)

    # os.system("ffmpeg -i video.mp4 -itsoffset 00:00:05 -i audio.mp3 -map 0:v -map 1:a -c:v copy -c:a aac -strict experimental output.mp4")

    return None





    