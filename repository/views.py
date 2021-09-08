from django.core import paginator
from django.http.response import HttpResponseRedirect
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
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
                s_repo['created_at'][0:10],
                s_repo['html_url']
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

        # Check if repo url was changed (for some reason)
        elif repo.url != s_repo['html_url']:
            repo.url = s_repo['html_url']
            repo.save()


@login_required(redirect_field_name='login')
def home_populate_repos(request):
    user = request.user

    request_starred_repos(request, user)

    return redirect('home_view')


@login_required(redirect_field_name='login')
def register_tag(request, repo_id):
    if request.method == 'POST':
        instance = get_object_or_404(Repository, repo_id=repo_id)
        form = RepositoryForm(request.POST or None, instance=instance)
        if form.is_valid():
            repo = form.save(commit=False)
            repo.save()
            form.save_m2m()
        else:
            instance.tags.clear()
    return HttpResponseRedirect(request.session['previous_page'])


@login_required(redirect_field_name='login')
def home_view(request):
    request.session['previous_page'] = request.path_info + "?p=" + request.GET.get("p", '1')

    user = User.objects.get(username=request.session['github_user'])
    repositories = Repository.objects.filter(user=user).order_by('-created_at_date')

    paginator = Paginator(repositories, 6)
    page = request.GET.get('p')
    repositories = paginator.get_page(page)

    common_tags = Repository.tags.most_common()[:5]
    context = {
        'repositories': repositories,
        'common_tags': common_tags,
        'github_login': user
    }
    return render(request, 'repository/home_view.html', context)
    

@login_required(redirect_field_name='login')
def tagged(request, slug):
    user = User.objects.get(username=request.session['github_user'])
    tag = get_object_or_404(Tag, slug=slug)
    # Filter posts by tag name
    repositories = Repository.objects.filter(
        tags=tag, user=user).order_by('-created_at_date')

    paginator = Paginator(repositories, 6)
    page = request.GET.get('p')
    repositories = paginator.get_page(page)

    common_tags = Repository.tags.most_common()[:5]
    context = {
        'tag':tag,
        'repositories': repositories,
        'github_login': user,
        'common_tags': common_tags,
    }
    return render(request, 'repository/tagged.html', context)


@login_required(redirect_field_name='login')
def search(request):
    term = request.GET.get('term')
    user = User.objects.get(username=request.session['github_user'])

    try:
        tag = Tag.objects.get(name__icontains=str(term))
    except:
        tag = None

    repositories = Repository.objects.filter(
        user=user).order_by('-created_at_date')

    if tag:
        repositories = repositories.filter(tags=tag)
    else:
        repositories = repositories.filter(name__icontains=term)

    paginator = Paginator(repositories, 6)
    page = request.GET.get('p')
    repositories = paginator.get_page(page)

    common_tags = Repository.tags.most_common()[:5]
    context = {
        'repositories': repositories,
        'common_tags': common_tags,
        'github_login': user
    }

    return render(request, 'repository/search.html', context)
