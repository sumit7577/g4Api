from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from moviepy.editor import *
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


@api_view(["GET", "POST"])
def videoEditor(request):
    if request.method == "POST":
        fileName = request.FILES["file"]
        complete = handle_uploaded_file(fileName)
        data = {}
        if complete:
            path = os.path.join(BASE_DIR, "static/", fileName.name)
            try:
                video = VideoFileClip(path)
                mp3 = video.audio
                if mp3 is not None:
                    mp3.write_audiofile("static/vid_audio.mp3")
                mp3_size = os.path.getsize("static/vid_audio.mp3")
                vid_size = os.path.getsize(path)
                bitrate = int((((vid_size - mp3_size)/video.duration)/1024*8))
                data["fps"] = video.fps
                data["duration"] = video.duration
                data["bitrate"] = str(bitrate)+" Kbps"
                data['resolution'] = str(
                    video.size[0]) + "*" + str(video.size[1])
                data["filename"] = fileName.name
                if os.path.exists(path):
                    os.remove(path)
                if os.path.exists("static/vid_audio.mp3"):
                    os.remove("static/vid_audio.mp3")
            except Exception as e:
                return JsonResponse({"success": False, "message": "Something Went Wrong!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return JsonResponse(data, status=status.HTTP_200_OK)
    return JsonResponse({"sucess": False, "message": "Get! Method Not Allowed"}, status=status.HTTP_400_BAD_REQUEST)


def handle_uploaded_file(f):
    with open(os.path.join(BASE_DIR, "static/", f.name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return True
