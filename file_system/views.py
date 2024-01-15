from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse, HttpResponseServerError
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.contrib import messages
from django.core.files.uploadedfile import SimpleUploadedFile, InMemoryUploadedFile


from GPSPhoto import gpsphoto
from google.cloud import vision
import os, io, json, base64, traceback
from io import BytesIO

#from openai import OpenAI

@login_required
def Tool(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        #gForm = GoogleVisionForm(request.POST, request.FILES)

        if form.is_valid():
            #image_files = request.image_files.getlist("image_file")

            #for image in image_files:
            image = form.save(commit=False)
            image.user = request.user
            filesize = image.image_file.size
                
            if filesize < 10485760:
                image.save()
            else:
                messages.error(request, "Failas virsija 10MB limita, failo dydis: " + str(filesize*1048576))
                return redirect('Toolpage')

            lat, lon = Extract_Exif(image.image_file.path)
            image.lat, image.lon = lat, lon
            image.save()

            gDescription, gLat, gLon, gScore, gLabel = Generate_Landmark_Info(image.image_file.path)
            gScore = int(gScore*100)
            #img_id = image.id
            google = GoogleVisionModel(description=gDescription, latitude=gLat, longitude=gLon, score=gScore, labels=gLabel, image_id = image.id)

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
        pass #jeigu nepavyko istraukti duomenu, lat ir lon tiesiog lieka su reiksmemis 0, bet programa neuzluta
    return lat, lon
#atliktu uzklausu generavimo funkcija, pasiimami visi objektai all()
@login_required
def ToolQueries(request):
    try:
        image = ImageUploadModel.objects.filter(user=request.user).all()
        #google = GoogleVisionModel.objects.filter(file=file)
        google = GoogleVisionModel.objects.filter(user=request.user).all()
        #unique labels
        #labels = GoogleVisionModel.objects.values_list(labels, flat=True)
    except:
        image = None
        google = None
        #labels = None

    context = {'image': image, 'google': google}#, 'labels':labels}
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
        else:
            messages.error(request, "Nepavyko pakeisti duomenų")
    context={'form':form, 'image': image}
        
    return render(request,'query-edit.html', context)

@login_required
def DeleteItem(request, image_id):#, google_id):
    try:
        image = ImageUploadModel.objects.filter(pk=image_id, user=request.user).first()
        google = GoogleVisionModel.objects.filter(pk=image_id, user=request.user).first()
        if image:
            os.remove(image.image_file.path)
            image.delete()
            google.delete()
            #GoogleVisionModel.objects.select_related().all().delete()
            #ImageUploadModel.objects.select_related().all().delete()
            #os.remove(image.image_file.path)
    except:
        messages.error(request, "Nepavyko ištrinti")
        return redirect('Toolqueries')
    return redirect('Toolqueries')

def Generate_Landmark_Info(image_file):
    desc, lat, long, score, label = "", 0, 0, 0, ""

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'GoogleAPI.json'
    client = vision.ImageAnnotatorClient()

    with io.open(image_file, "rb") as file:
        content = file.read()
    image = vision.Image(content=content)

    #features = [
    #    {"type": vision.Feature.Type.LANDMARK_DETECTION},
    #    {"type": vision.Feature.Type.LABEL_DETECTION},
    #]
    #response = client.landmark_detection(image=image), features=features)

    try:
        response = client.landmark_detection(image=image)
        desc, lat, long, score = Get_Landmarks(response)
    except:
        HttpResponse("Ivyko klaida, nepavyko gauti duomenu is GoogleCloud")
    try:
        response = client.label_detection(image=image)
        label = Get_Labels(response)
    except:
        HttpResponse("Ivyko klaida, nepavyko gauti duomenu is GoogleCloud")

    return desc, lat, long, score, label

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
        HttpResponse("Ivyko klaida, nepavyko gauti duomenu is GoogleCloud")
    return desc, lat, long, score#, top_label

def Get_Labels(response: vision.AnnotateImageResponse, min_score: float = 0.5):
    top_label = []

    try:
        labels = response.label_annotations
        if labels:
            for label in labels:
                if label.score > min_score:
                    top_label.append(label.description)
                    if len(top_label) == 10:
                        break
            return top_label
        else:
            HttpResponse("Ivyko klaida, nepavyko gauti duomenu is GoogleCloud")
    except:
        HttpResponse("Ivyko klaida, nepavyko gauti duomenu is GoogleCloud")

@login_required
def MapCreate(request):
    if request.method == 'POST':
        waypoints_json = request.POST.get('waypoints')
        waypoints = json.loads(waypoints_json)
        #print('Received Waypoints:', waypoints)
        
        map_name = request.POST.get('map_name')
        map_description = request.POST.get('map_description')

        map_model = MapCreation.objects.create(
            user=request.user,
            map_name=map_name,
            map_description=map_description
        )

        for waypoint in waypoints:

            image_file = waypoint.get('imageFile', None)

            if image_file:
                image_name = waypoint.get('title')
                notes = waypoint.get('description')
                latitude = waypoint.get('latitude')
                longitude = waypoint.get('longitude')

                #nuotraukos convert i base64, jog sia atvaizduoti waypointse, pries pilnai ikeliant ft i db
                if isinstance(image_file, str): 
                    image_data = base64.b64decode(image_file.split(",")[1])
                    uploaded_image = InMemoryUploadedFile(
                        file=BytesIO(image_data),
                        field_name=None,
                        name=f"{image_name}.jpg",
                        content_type="image/jpeg",
                        size=len(image_data),
                        charset=None,
                    )
                #kuriant visiskai nauja zyme per leaflet.draw ikeliama ft
                else:
                    uploaded_image = SimpleUploadedFile(image_name, image_file.read(), content_type="image/jpeg")
                image_upload = ImageUploadModel.objects.create(
                    user=request.user,
                    image_name=image_name,
                    image_file=uploaded_image,
                    notes=notes,
                    lat=latitude,
                    lon=longitude
                )
            else:
                image_upload = None

            #print(ImageUploadModel.pk)
                
            #zymes sauganciam modeliui/lentelei DB, sudaromi irasai kiek yra zymiu
            MapPointers.objects.create(
                map_model=map_model,
                latitude=waypoint.get('latitude'),
                longitude=waypoint.get('longitude'),
                title=waypoint.get('title', ''),
                description=waypoint.get('description', ''),
                image_upload=image_upload,
                user=request.user,
            )
            return redirect('Mapview')

    image = ImageUploadModel.objects.filter(user=request.user).all()
    google = GoogleVisionModel.objects.filter(user=request.user).all()

    context = {'image': image, 'google': google}
    return render(request, 'mapcreate.html', context)

@login_required
def GetWaypoints(request, map_model_id):
    try:
        waypoints = MapPointers.objects.filter(map_model_id=map_model_id).values('title', 'description', 'latitude', 'longitude', 'image_upload_id')
        waypoints_list = list(waypoints)
        return JsonResponse(waypoints_list, safe=False)
    except:
        messages.error(request, "Ivyko klaida, nepavyko gauti zymiu duomenu")
    
@login_required
def MapView (request):
    try:
        image = ImageUploadModel.objects.filter(user=request.user).all()
        google = GoogleVisionModel.objects.filter(user=request.user).all()
        maps = MapCreation.objects.filter(user=request.user).all()
        waypoints = MapPointers.objects.filter(user=request.user).all()
    #except:
    #    image = None
    #    google = None
    #    maps = None
    #    waypoints = None
    except Exception as e:
        #message = traceback.format_exc()
        messages.error(request, e)
        return redirect('Mapview')

    context = {'image': image, 'google': google, 'maps':maps, 'waypoints':waypoints} #{'mapdata': mapdata}#
    return render(request, 'mapview.html', context)


@login_required
def DeleteMap(request, map_id):
    try:
        map = MapCreation.objects.filter(pk=map_id, user=request.user).first()
        pointers = MapPointers.objects.filter(map_model_id=map_id,  user=request.user).first()
        if pointers.map_model_id == map_id:
            pointers.delete()

        if map:
            #for pointer in pointers:
            #    pointer.delete()
            map.delete()
    except Exception as e:
        #message = traceback.format_exc()
        #print(message)
        messages.error(request, e)
        return redirect('Mapview')
    return redirect('Mapview')

#@login_required
#def TravelAssistant(request):
#    openai_client = OpenAI(api_key=os.environ['OPEN_AI'])
#    assistant = openai_client.beta.assistants.create(
#        name = 'TravelGuide',
#        instructions = 'When given JSON, you need to generate back a list of 10 places of interest based on given locations for traveling guide  in JSON format: object, latitude and longitude.',
#        tools = [{}]
#    )