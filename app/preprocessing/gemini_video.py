import os
import shutil

import cv2
import dotenv
import google.generativeai as genai

# Add .env variables anywhere before SECRET_KEY
dotenv_file = os.path.join(".", ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

# Set the API key
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
genai.configure(api_key=GEMINI_API_KEY)


# video_file_name = "https://download.blender.org/peach/bigbuckbunny_movies/BigBuckBunny_320x180.mp4"
file_url = (
    "https://download.blender.org/peach/bigbuckbunny_movies/BigBuckBunny_320x180.mp4"
)

# video_file_name = f"{file_url}"


# Create or cleanup existing extracted image frames directory.
FRAME_EXTRACTION_DIRECTORY = "C:/MHacks 2024/VibeSync/app/static/app/images/content/frames/"
FRAME_PREFIX = "_frame"


class Video:
    def __init__(self, system_instruction):
        self.system_instruction = system_instruction

    def create_frame_output_dir(output_dir):
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        else:
            shutil.rmtree(output_dir)
            os.makedirs(output_dir)

    def extract_frame_from_video(video_file_path):
        print(
            f"Extracting {video_file_path} at 1 frame per second. This might take a bit..."
        )
        Video.create_frame_output_dir(FRAME_EXTRACTION_DIRECTORY)
        vidcap = cv2.VideoCapture(video_file_path)
        fps = vidcap.get(cv2.CAP_PROP_FPS)
        frame_duration = 1 / fps  # Time interval between frames (in seconds)
        output_file_prefix = os.path.basename(video_file_path).replace(".", "_")
        frame_count = 0
        count = 0
        while vidcap.isOpened():
            success, frame = vidcap.read()
            if not success:  # End of video
                break
            if int(count / fps) == frame_count:  # Extract a frame every second
                min = frame_count // 60
                sec = frame_count % 60
                time_string = f"{min:02d}:{sec:02d}"
                image_name = f"{output_file_prefix}{FRAME_PREFIX}{time_string}.jpg"
                output_filename = os.path.join(FRAME_EXTRACTION_DIRECTORY, image_name)
                cv2.imwrite(output_filename, frame)
                frame_count += 1
            count += 1
        vidcap.release()  # Release the capture object\n",
        print(f"Completed video frame extraction!\n\nExtracted: {frame_count} frames")

        return None

    # # List files uploaded in the API
    # for n, f in zip(range(len(uploaded_files)), genai.list_files()):
    #   print(f.uri)

    def make_request(prompt, files):
        request = [prompt]
        for file in files:
            request.append(file.timestamp)
            request.append(file.response)
        return request

    def call_gemini(self, video_url):
        Video.extract_frame_from_video(video_url)
        # Create the prompt.
        prompt = "Describe this video."

        # Set the model to Gemini 1.5 Pro.
        model = genai.GenerativeModel(
            model_name="models/gemini-1.5-pro-latest",
            system_instruction=self.system_instruction,
        )

        # Make GenerateContent request with the structure described above.

        uploaded_files = File.process_frame()
        # Make the LLM request.
        request = Video.make_request(prompt, uploaded_files)
        response = model.generate_content(request, request_options={"timeout": 600})
        print(response.text)

        print(f"Deleting {len(uploaded_files)} images. This might take a bit...")
        for file in uploaded_files:
            genai.delete_file(file.response.name)
            print(f"Deleted {file.file_path} at URI {file.response.uri}")
        print(f"Completed deleting files!\n\nDeleted: {len(uploaded_files)} files")
        return response


class File:
    def __init__(self, file_path: str, display_name: str = None):
        self.file_path = file_path
        if display_name:
            self.display_name = display_name
        self.timestamp = File.get_timestamp(file_path)

    def set_file_response(self, response):
        self.response = response

    def get_timestamp(filename):
        """Extracts the frame count (as an integer) from a filename with the format
        'output_file_prefix_frame00:00.jpg'.
        """
        parts = filename.split(FRAME_PREFIX)
        if len(parts) != 2:
            return None  # Indicates the filename might be incorrectly formatted
        return parts[1].split(".")[0]

    def process_frame():
        # Process each frame in the output directory
        files = os.listdir(FRAME_EXTRACTION_DIRECTORY)
        files = sorted(files)
        files_to_upload = []
        for file in files:
            files_to_upload.append(
                File(file_path=os.path.join(FRAME_EXTRACTION_DIRECTORY, file))
            )

        # Upload the files to the API
        # Only upload a 10 second slice of files to reduce upload time.
        # Change full_video to True to upload the whole video.
        full_video = True

        uploaded_files = []
        print(
            f"Uploading {len(files_to_upload) if full_video else 10} files. This might take a bit..."
        )

        for file in files_to_upload if full_video else files_to_upload[40:50]:
            print(f"Uploading: {file.file_path}...")
            response = genai.upload_file(path=file.file_path)
            file.set_file_response(response)
            uploaded_files.append(file)

        print(f"Completed file uploads!\n\nUploaded: {len(uploaded_files)} files")
        return uploaded_files