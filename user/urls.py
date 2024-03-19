from django.contrib import admin
from django.urls import path
from user import views

urlpatterns = [
    path("", views.index, name='user'),
    path("signup", views.signup, name='signup'),
    path("login", views.login, name='login'),
    path("home", views.home, name='home'),
]