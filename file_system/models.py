from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class ImageUploadModel (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    image_name = models.CharField('Failo pavadinimas',max_length=50, null=True)
    image_file = models.ImageField('Įkelkite failą',upload_to='images/', null=True)
    notes = models.TextField('Užrasai', max_length=500, null=True)
    lat = models.DecimalField(max_digits=30, decimal_places=15, null=True)
    lon = models.DecimalField(max_digits=30, decimal_places=15, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, null=True)

class GoogleVisionModel (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True )
    description = models.CharField(max_length=50, null=True)
    latitude = models.CharField(max_length=50, null=True)
    longitude = models.CharField(max_length=50, null=True)
    score = models.DecimalField(max_digits=30, decimal_places=0, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True, null=True)