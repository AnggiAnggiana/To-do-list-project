from django.contrib.auth.models import User
from django.contrib.auth import login
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import SignUpForm
from django.urls import reverse
# from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout

# login with google
from social_django.utils import psa

from django.http import HttpResponse
from social_django.views import complete as social_auth_complete


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()

            subject = 'Aktivasi akun anda'
            message = render_to_string('activation_email.html', {
                'user': user,
                'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user)
            })

            user.email_user(subject,message)
            messages.success(request, 'Silahkan cek email anda untuk aktivasi')
            return redirect(reverse('login'))
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form' : form})
        

def activate(request, uidb64, token):
    uid  = urlsafe_base64_decode(uidb64).decode()
    user = User.objects.get(pk=uid)

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_validated = True
        user.save()

        login(request, user)
        messages.success(request, 'Akun berhasil diaktifkan')
        return redirect('login')
    else:
        messages.error(request, 'Aktivasi gagal')
        return redirect(reverse('login'))
    
    
def login_user(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return(redirect('todo_list'))
        else:
            messages.success(request, ('Login tidak berhasil, ada kesalahan username atau password'))
            return(redirect('login'))
    else:
        return render(request, 'accounts/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, ('Kamu sudah berhasil keluar, silahkan login kembali'))
    return(redirect('login'))


@psa('social:complete')
def GoogleLoginView(request, backend, *args, **kwargs):
    if request.user.is_authenticated:
        return redirect('todo_list')
    elif isinstance(backend, str):
        return social_auth_complete (request, backend, *args, **kwargs)
    else:
        return HttpResponse("Invalid backend")
