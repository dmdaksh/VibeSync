from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
# Create your views here.

def upload_video(request):
    if request.method == "POST":
        video_file = request.FILES.get('video', '')
        if video_file:
            fs = FileSystemStorage()
            filename = fs.save(video_file.name, video_file)
            uploaded_file_url = fs.url(filename)
            return JsonResponse({'message': 'Success', 'fileUrl': uploaded_file_url}, status=200)
        else:
            return JsonResponse({'message': 'No file provided'}, status=400)
                # get file from form
            # save video and call gemini api

    return render(request, 'app/index.html')
