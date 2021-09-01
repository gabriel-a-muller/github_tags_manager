from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from social_django.models import UserSocialAuth

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