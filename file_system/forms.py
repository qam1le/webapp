from django import forms
from .models import *

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUploadModel
        fields = ('image_name', 'image_file',)# 'lat', 'lon')

class GoogleVisionForm(forms.ModelForm):
     class Meta:
        model = GoogleVisionModel
        fields = '__all__'