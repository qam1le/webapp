from django.contrib import admin

# Register your models here.
from .models import ImageUploadModel
admin.site.register(ImageUploadModel)