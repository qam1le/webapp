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
    path('mapcreate/', MapCreate, name='Mapcreate'),
    path('get_waypoints/<int:map_model_id>/', GetWaypoints, name='GetWaypoints'),
    path('mapview/', MapView, name='Mapview'),
    #path('save_waypoints/', save_waypoints, name='save_waypoints'),
    #path('save_map/', save_map_view, name='save_map_view'),
    path('images/delete/<int:image_id>/', DeleteItem, name='Deleteitem'),
    path('mapdelete/<int:map_id>', DeleteMap, name='Deletemap'),
    path('logout/', views.Logout, name='Logout'),
]