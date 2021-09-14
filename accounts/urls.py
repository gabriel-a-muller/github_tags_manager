from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.login, name='index_login'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    # path('register/', views.register, name='register'),
    re_path(r'settings/$', views.settings, name='settings'),
    re_path(r'^settings/password/$', views.password, name='password'),
]