from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class ImageUploadModel (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    image_name = models.CharField('Failo pavadinimas',max_length=50, null=True)
    image_file = models.ImageField('Ikelkite faila',upload_to='images/', null=True)
    notes = models.TextField('Uzrasai', max_length=500, null=True)
    lat = models.DecimalField(max_digits=30, decimal_places=15, null=True)
    lon = models.DecimalField(max_digits=30, decimal_places=15, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, null=True)

class GoogleVisionModel (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    image = models.OneToOneField(ImageUploadModel, on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=50, null=True)
    latitude = models.CharField(max_length=50, null=True)
    longitude = models.CharField(max_length=50, null=True)
    score = models.DecimalField(max_digits=30, decimal_places=0, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, null=True)
    labels = models.JSONField(max_length=1024, null=True)

class MapCreation (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    #upload_model = models.ManyToManyField(ImageUploadModel, related_name='uploadmodel', blank=True)
    #vision_model = models.ManyToManyField(GoogleVisionModel, related_name='visionmodel', blank=True)
    map_name = models.CharField(max_length=50, null=True)
    map_description = models.CharField(max_length=500, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

class MapPointers (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    map_model = models.ForeignKey(MapCreation, on_delete=models.CASCADE)
    latitude  = models.DecimalField(max_digits=30, decimal_places=15) #was floatfield
    longitude  = models.DecimalField(max_digits=30, decimal_places=15)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    image_upload = models.ForeignKey(ImageUploadModel, on_delete=models.SET_NULL, null=True, blank=True)