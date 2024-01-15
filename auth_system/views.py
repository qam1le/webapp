from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.password_validation import *
from django.core.exceptions import ValidationError

from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.db.models.query_utils import Q
from .forms import *
# Create your views here.

ALLOWED_EMAILS = ['gmail.com', 'yahoo.com', 'outlook.com', 'proton.me', 'icloud.com']

def Index(request):
    return render(request, 'index.html', {})

def Register(request):
    #if request.user.is_authenticated:
    #    return redirect('Homepage')
    
    if request.method == 'POST':
        mail = request.POST.get('email')
        
        if not any(mail.endswith(emails) for emails in ALLOWED_EMAILS):
            messages.error(request, "Klaida. Netinkamas el pasto domenas, naudokite @gmail.com arba panašias alternatyvas")
            return redirect('Register')
        
        uname = request.POST.get('username')
        psw = request.POST.get('password')
        psw_r = request.POST.get('password-repeat')

        try:
            if validate_password(psw, user=None, password_validators=None):
                pass
        except Exception as e:
            messages.error(request, e)
            return redirect('Register')

        if User.objects.filter(username=uname).exists() or User.objects.filter(email=mail).exists():
            messages.error(request, "Klaida. Vartotojas jau egzistuoja")
            return redirect('Register')
        else:
            if psw == psw_r:
                user = User.objects.create_user(username=uname, email=mail, password=psw)
                user.is_active = False
                user.save()
                activateEmail(request, user, mail)
                return redirect('Login')
            else:
                messages.error(request, 'Nevienodi slaptazodziai')
                return redirect('Register')
    
    return render(request, 'register.html', {})

def activateEmail(request, user, to_email):
    mail_subject = 'Paskyros aktyvavimas.'
    message = render_to_string('activation.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, 'Sekmingai sukurta paskyra, prasome patikrinti el. pasta, jog uzbaigtumete registracija :)')
    else:
        messages.error(request, 'Problemos su patvirtinimo laisko issiuntimo, patikrinkite ar suvedete duomenis teisingai')

def ChangePassword(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = request.POST.get('username')
        resetPassword(request,user,email)

def resetPassword(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            mail = form.cleaned_data['email']
            user = get_user_model().objects.filter(Q(email=mail)).first()
            if user:
                mail_subject = 'Slaptažodžio keitimas.'
                message = render_to_string('resetpswemail.html', {
                'user': user,
                'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
                'protocol': 'https' if request.is_secure() else 'http'        
            })
            email = EmailMessage(mail_subject, message, to=[user.email])  
            if email.send():
                messages.success(request, 'Instrukcijos nusiųstos, nurodytu el paštu')
            else:
                messages.error(request, 'Nepavyko išsiųsti instrukcijų nurodytu el. paštu, ar teisingai suvedėte duomenis?')
        return redirect('Login')
    return render(request, 'forgotpsw.html', {})

def confirmReset(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            psw = request.POST.get('password')
            psw_r = request.POST.get('password-repeat')
            if psw == psw_r:
                user.save()
                messages.success(request, 'Sekmingai pakeistas slaptazodis')
                return redirect('Login')
        return render(request, 'psweditconfirm.html')
    else:
        messages.error(request, 'Nuoroda nera veikianti!')
    
    return redirect('Login')


def Activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, 'Sekmingai patvirtinta paskyra. Galite prisijungti')
        return redirect('Login')
    else:
        messages.error(request, 'Nuoroda nera veikianti!')
    
    return redirect('Homepage')



def Login(request):
    if request.user.is_authenticated:
        return redirect('Homepage')
    
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