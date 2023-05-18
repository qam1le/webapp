from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from auth_system import views

urlpatterns = [
    path('tool/', Tool, name='Toolpage'),
    #path('imgup/', Image_Upload, name='Imgupload'),
    path('queries/', ToolQueries, name='Toolqueries'),
    #path('imgview/', Image_Display, name='Imgdisplay'),
    #path('images/<int:image_id>/', ViewItem, name='Viewitem'),
    path('images/delete/<int:image_id>/', DeleteItem, name='Deleteitem'),
    path('logout/', views.Logout, name='Logout'),
]