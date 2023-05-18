from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.contrib import messages

from GPSPhoto import gpsphoto

@login_required
def Tool(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user
            image.save()
            
            try:
                lat, lon = Extract_Exif(image.image_file.path)
                image.lat, image.lon = lat, lon
                image.save()
            except:
                lat, lon = 0, 0

            #form.save()
            #try:
            #    data = gpsphoto.getGPSData(str(image.image_file))
            #    image.lat = data['Latitude']
            #    image.lon = data['Longitude']
            #    image.save()
            #except:
            #    pass
            return redirect('Toolpage')
    else:
        form = ImageUploadForm()
    
    #jeigu naujas vartotojas arba nera nieko ikeles, puslapis uzlus.:( apsauga nuo to
    try:
        image = ImageUploadModel.objects.filter(user=request.user).latest('uploaded_at')
    except:
        image = None
    return render(request, 'analysis.html', {'form':form, 'image':image})

@login_required
def Extract_Exif(image):
    data = gpsphoto.getGPSData(image)
    lat = 0
    lon = 0
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
    except:
        image = None
    return render(request, 'queries-list.html', {'image': image})

@login_required
def ViewItem(request, image_id):
    try: 
        #image = ImageUploadModel.objects.filter(pk=image_id, user=request.user)
        pass
    except:
        pass
        #HttpResponse("Nepavyko:(")
    #return redirect('Toolpage')

@login_required
def DeleteItem(request, image_id):
    try:
        image = ImageUploadModel.objects.filter(pk=image_id, user=request.user).first()
        if image:
            image.delete()
    except:
        HttpResponse("Ivyko klaida?")
    return redirect('Toolqueries')