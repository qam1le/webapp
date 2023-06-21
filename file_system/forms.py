from django import forms
from .models import *
from django.forms import TextInput

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUploadModel
        fields = ('image_name', 'image_file', 'notes')# 'lat', 'lon')
        widgets = {
            'image_name': TextInput(attrs={
                'class': "form-control"
            }),
            'notes': TextInput(attrs={
                'class': "form-control",
                'style': "height:128px;"
            })
        }

class GoogleVisionForm(forms.ModelForm):
     class Meta:
        model = GoogleVisionModel
        fields = '__all__'