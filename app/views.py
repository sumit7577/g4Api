from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework import status
from moviepy.editor import *
from pathlib import Path
import hashlib
from app import neo


BASE_DIR = Path(__file__).resolve().parent.parent
print(BASE_DIR)


@api_view(["GET", "POST"])
def videoEditor(request):
    if request.method == "POST":
        fileName = request.FILES["file"]
        complete = handle_uploaded_file(fileName)
        data = {}
        if complete:
            path = os.path.join(BASE_DIR, "static/", fileName.name)
            md5 = hashlib.md5(open(path,'rb').read()).hexdigest()

            if fileName.name.endswith(".h264") or fileName.name.endswith(".webm"):
                outputPath= os.path.join(BASE_DIR, "static/outputVideo.mp4")
                os.system(f'ffmpeg -i {path} {outputPath}')
                os.remove(path)
                path = outputPath

            mp3_path = os.path.join(BASE_DIR,"static/vid_audio.mp3")
            try:
                video = VideoFileClip(path)
                mp3 = video.audio
                if mp3 is not None:
                    mp3.write_audiofile(mp3_path)
                    mp3_size = os.path.getsize(mp3_path)
                    vid_size = os.path.getsize(path)
                    bitrate = int((((vid_size - mp3_size)/video.duration)/1024*8))
                    audioTracks = os.system(f"ffprobe -show_format -show_streams -i {path} | grep Audio")
                    
                vid_size = os.path.getsize(path)
                bitrate = int((((vid_size)/video.duration)/1024*8))
                data["fps"] = video.fps
                data["duration"] = video.duration
                data["bitrate"] = str(bitrate)+" Kbps"
                data["success"] = True
                data["md5"] = md5
                data['resolution'] = str(video.size[0]) + "*" + str(video.size[1])
                data["filename"] = fileName.name
                if os.path.exists(path):
                    os.remove(path)
                if os.path.exists(mp3_path):
                    os.remove(mp3_path)
            except Exception as e:
                print(e)
                return JsonResponse({"success": False, "message": "Something Went Wrong!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return JsonResponse(data, status=status.HTTP_200_OK)
    return JsonResponse({"sucess": False, "message": "Get! Method Not Allowed"}, status=status.HTTP_400_BAD_REQUEST)


def handle_uploaded_file(f):
    with open(os.path.join(BASE_DIR, "static/", f.name), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return True


@api_view(["GET"])
def home(request):
    try:
        api_data = neo.client.get_api_data()
        return JsonResponse({"Success":True,"message":api_data},status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return JsonResponse({"Success": False, "message": "Something went wrong!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


