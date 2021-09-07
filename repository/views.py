import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from taggit.models import Tag

from . forms import RepositoryForm
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
        try:
            repo = Repository.objects.get(repo_id=s_repo['id'], user=user)
        except:
            repo = None
        # Check if not exists before creating new record
        if not repo:
            repo = Repository.objects.create_repository(
                s_repo['name'],
                user,
                s_repo['id'],
                s_repo['description'],
                s_repo['created_at'][0:10]
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
def home_populate_repos(request):
    user = request.user

    request_starred_repos(request, user)

    return redirect('home_view')


def register_tag(request, repo_id):
    if request.method == 'POST':
        print("REPO_ID: ", repo_id)
        instance = Repository.objects.get(repo_id=repo_id)
        form = RepositoryForm(request.POST or None, instance=instance)
        if form.is_valid():
            repo = form.save(commit=False)
            repo.save()
            form.save_m2m()
        else:
            instance.tags.clear()
    return redirect('home_view')

def home_view(request):
    user = User.objects.get(username=request.session['github_user'])
    repositories = Repository.objects.filter(user=user).order_by('-created_at_date')
    common_tags = Repository.tags.most_common()[:5]
    context = {
        'repositories': repositories,
        'common_tags': common_tags,
        'github_login': user
    }

    return render(request, 'repository/home_view.html', context)

def tagged(request, slug):
    github_login = request.session['github_user'] if request.session['github_user'] else None
    tag = get_object_or_404(Tag, slug=slug)
    # Filter posts by tag name  
    repositories = Repository.objects.filter(tags=tag)
    common_tags = Repository.tags.most_common()[:5]
    context = {
        'tag':tag,
        'repositories': repositories,
        'github_login': github_login,
        'common_tags': common_tags,
    }
    return render(request, 'repository/home_view.html', context)
