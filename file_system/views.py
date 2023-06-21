from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.contrib import messages
from pathlib import Path

from GPSPhoto import gpsphoto
from google.cloud import vision
import os, io

@login_required
def Tool(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        #gForm = GoogleVisionForm(request.POST, request.FILES)

        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user
            filesize = image.image_file.size

            if filesize < 5242880:
                image.save()
            else:
                messages.error(request, "Nuh-uh")
                return redirect('Toolpage')

            lat, lon = Extract_Exif(image.image_file.path)
            image.lat, image.lon = lat, lon
            image.save()

            gDescription, gLat, gLon, gScore = Generate_Landmark_Info(image.image_file.path)
            gScore = int(gScore*100)
            google = GoogleVisionModel(description=gDescription, latitude=gLat, longitude=gLon, score=gScore)
            google.user = request.user
            google.save()

            return redirect('Toolpage')
    else:
        form = ImageUploadForm()
    #jeigu naujas vartotojas arba nera nieko ikeles, puslapis uzlus.:( apsauga nuo to
    try:
        image = ImageUploadModel.objects.filter(user=request.user).latest('uploaded_at')
        google = GoogleVisionModel.objects.filter(user=request.user).latest('uploaded_at')
    except:
        image = None
        google = None
    context = {'form':form, 'image':image, 'google':google}
    return render(request, 'analysis.html', context)

#@login_required
def Extract_Exif(image):
    data = gpsphoto.getGPSData(image)
    lat, lon = 0, 0
    try:
        lat = data['Latitude']
        lon = data['Longitude']
    except:
        pass
    return lat, lon
#atliktu uzklausu generavimo funkcija, pasiimami visi objektai all()
@login_required
def ToolQueries(request):
    try:
        image = ImageUploadModel.objects.filter(user=request.user).all()
        google = GoogleVisionModel.objects.filter(user=request.user).all()
    except:
        image = None
        google = None

    context = {'image': image, 'google': google}
    return render(request, 'queries-list.html', context)

@login_required
def EditItem(request, image_id):
    image = ImageUploadModel.objects.get(pk=image_id, user=request.user)
    form = ImageUploadForm(instance=image)

    if request.method == "POST":
        form = ImageUploadForm(request.POST, instance=image)
        if form.is_valid():
            form.save()
            messages.success(request,'Sėkmingai pakeisti duomenys')
            return redirect('Toolqueries')
    context={'form':form, 'image': image}

    return render(request,'query-edit.html', context)

@login_required
def DeleteItem(request, image_id):#, google_id):
    try:
        image = ImageUploadModel.objects.filter(pk=image_id, user=request.user).first()
        if image:
            image.delete()
            GoogleVisionModel.objects.select_related().all().delete()
            os.remove(image.image_file.path)
    except:
        HttpResponse("Ivyko klaida")
    return redirect('Toolqueries')


def Generate_Landmark_Info(image_file):
    desc, lat, long, score = "", 0, 0, 0


    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'/home/sudokewl/webapp/GoogleAPI.json'
    client = vision.ImageAnnotatorClient()


    with io.open(image_file, "rb") as file:
        content = file.read()
    image = vision.Image(content=content)
    response = client.landmark_detection(image=image)

    try:
        desc, lat, long, score = Get_Landmarks(response)
    except:
        pass
    return desc, lat, long, score

def Get_Landmarks(response: vision.AnnotateImageResponse, min_score: float = 0.5):
    lat, long, score, max_score = 0, 0, 0, None
    desc = ""

    try:
        for landmark in response.landmark_annotations:
            if landmark.score < min_score:
                continue

            if isinstance(landmark.score, float):
                if max_score is None or landmark.score > max_score:
                    max_score = landmark.score

            if landmark.score == max_score:
                lat = landmark.locations[0].lat_lng.latitude
                long = landmark.locations[0].lat_lng.longitude
                desc = landmark.description
                score = landmark.score
    except:
        pass
    return desc, lat, long, score