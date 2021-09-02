import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from social_django.models import UserSocialAuth

from . models import Repository

def request_starred_repos(request, user):
    try:
        starred_repos = requests.get(
        'https://api.github.com/users/{user}/starred'.format(user=user)
        )
        starred_repos.raise_for_status()
    except requests.exceptions.RequestException as err:
        messages.error(request, err)
        return
    except requests.exceptions.HTTPError as err:
        messages.error(request, err)
        return

    # For each starred repo
    for s_repo in starred_repos.json():
        repo = Repository.objects.get(repo_id=s_repo['id'], user_id=user)
        # Check if not exists before creating new record
        if not repo:
            repo = Repository.objects.create_repository(
                s_repo['name'],
                user,
                s_repo['id'],
                s_repo['description']
            )
            repo.save()
        # Check if repo name was changed
        elif repo.name != s_repo['name']:
            repo.name = s_repo['name']
            repo.save()
        # Check if repo description was changed
        elif repo.description != s_repo['description']:
            repo.description = s_repo['description']
            repo.save()


@login_required(redirect_field_name='login')
def home(request):
    user = request.user

    request_starred_repos(request, user)

    try:
        github_login = user.social_auth.get(provider='github')
    except UserSocialAuth.DoesNotExist:
        github_login = None

    return render(request, 'accounts/home.html', {
        'github_login': github_login
    })