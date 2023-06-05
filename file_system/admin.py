from django.contrib import admin

# Register your models here.
from .models import ImageUploadModel, GoogleVisionModel
admin.site.register(ImageUploadModel)
admin.site.register(GoogleVisionModel)