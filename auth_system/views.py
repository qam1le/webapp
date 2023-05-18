from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

def Index(request):
    return render(request, 'index.html', {})

def Register(request):
    if request.user.is_authenticated:
        return redirect('Homepage')
    
    if request.method == 'POST':
        mail = request.POST.get('email')
        uname = request.POST.get('username')
        psw = request.POST.get('password')
        psw_r = request.POST.get('password-repeat')
        if User.objects.filter(username=uname).exists() or User.objects.filter(email=mail).exists():
            messages.error(request, "Klaida. Vartotojas jau egzistuoja")
            return redirect('Register')
        else:
            if psw == psw_r:
                user = User.objects.create_user(username=uname, email=mail, password=psw)
                user.save()
                return redirect('Login')
            else:
                return HttpResponse('Neteisingas slap')
    
    return render(request, 'register.html', {})

def Login(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        psw = request.POST.get('password')

        user = authenticate(request, username=name, password=psw)
        if user is not None:
            login(request, user)
            return redirect('Homepage')
        else:
            messages.error(request, "Vartotojas neegzistuoja")
            return redirect('Login')
    return render(request, 'login.html', {})

@login_required
def Homepage(request):
    return render(request, 'homepage.html', {})

@login_required
def Logout(request):
    logout(request)
    return redirect('Index')