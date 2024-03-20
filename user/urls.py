from django.contrib import admin
from django.urls import path
from user import views
from .views import ai_response

urlpatterns = [
    path("", views.index, name='user'),
    path("signup", views.signup, name='signup'),
    path("login", views.login, name='login'),
    path("", views.intelliAi, name='intelliAi'),
    path('ai-response/', ai_response, name='ai_response'),
]