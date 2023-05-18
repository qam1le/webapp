from django import forms
from .models import ImageUploadModel

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUploadModel
        fields = ('image_name', 'image_file',)# 'lat', 'lon')