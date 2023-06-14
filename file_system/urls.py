from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *
from auth_system import views

urlpatterns = [
    path('tool/', Tool, name='Toolpage'),
    path('queries/', ToolQueries, name='Toolqueries'),
    path('edit/<int:image_id>/', EditItem, name='Edititem'),
    #path('images/<int:image_id>/', EditItem, name='Edititem'),
    path('images/delete/<int:image_id>/', DeleteItem, name='Deleteitem'),
    path('logout/', views.Logout, name='Logout'),
]