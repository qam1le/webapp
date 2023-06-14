from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('index/', Index, name='Index'),
    path('register/', Register, name='Register'),
    path('login/', Login, name='Login'),
    path('activate/<uidb64>/<token>', Activate, name='Activate'),

    path('home/', Homepage, name='Homepage'),
    path('logout/', Logout, name='Logout'),
    
    #path('reset_password', resetPassword, name='Resetpswd'),
    #path('reset/<uidb64>/<token>', confirmReset, name='Resetconfirm'),
]