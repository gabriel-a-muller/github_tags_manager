from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, login
from django.contrib.auth.decorators import login_required
from social_django.utils import psa
from social_django.models import UserSocialAuth

def login(request):
    return render(request, 'accounts/login.html')

@login_required(redirect_field_name='login')
def logout(request):
    auth.logout(request)
    return redirect('login')

def register(request):
    return render(request, 'accounts/register.html')

@login_required(redirect_field_name='login')
def home(request):
    user = request.user

    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None

    return render(request, 'accounts/home.html', {
        'github_login': github_login
    })

@login_required(redirect_field_name='login')
def settings(request):
    user = request.user

    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'accounts/settings.html', {
        'github_login': github_login,
        'can_disconnect': can_disconnect
    })

@login_required(redirect_field_name='login')
def password(request):
    if request.user.has_usable_password():
        PasswordForm = PasswordChangeForm
    else:
        PasswordForm = AdminPasswordChangeForm

    if request.method == 'POST':
        form = PasswordForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordForm(request.user)
    return render(request, 'accounts/password.html', {'form': form})