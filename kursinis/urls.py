"""
URL configuration for kursinis project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from auth_system import views as authviews
from file_system import views as fileviews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', authviews.Index, name="Index"),
    path('register/', authviews.Register, name='Register'),
    path('login/', authviews.Login, name='Login'),
    path('activate/<uidb64>/<token>', authviews.Activate, name='Activate'),

    path('home/', authviews.Homepage, name='Homepage'),
    path('tool/', fileviews.Tool, name='Toolpage'),
    path('queries/', fileviews.ToolQueries, name='Toolqueries'),
    path('edit/<int:image_id>/', fileviews.EditItem, name='Edititem'),
    path('images/delete/<int:image_id>/', fileviews.DeleteItem, name='Deleteitem'),
    path('logout/', authviews.Logout, name='Logout'),

    #path('reset_password', authviews.resetPassword, name='Resetpswd'),
    #path('reset/<uidb64>/<token>', authviews.confirmReset, name='Resetconfirm'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
