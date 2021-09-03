from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('home/', views.home_populate_repos, name='home'),
    path('register_tag/<int:repo_id>', views.register_tag, name='register_tag'),
    path('home_view/', views.home_view, name='home_view'),
    path('tag/<slug:slug>/', views.tagged, name="tagged"),
]