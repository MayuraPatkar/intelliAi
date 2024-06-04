from django.urls import path
from user import views

urlpatterns = [
    path("", views.index, name='user'),
    path("signup/", views.signup, name='signup'),
    path("login/", views.user_login, name='login'),
    path("", views.intelliAi, name='intelliAi'),
    path('get_chat_history/', views.get_conve_history, name='get_conve_history'),
    path('ai-response/', views.ai_response, name='ai_response'),
    path('logout/', views.logout, name='logout'),
    path('clear-data/', views.clear_data, name='clear-data'),
    path('kill-account/', views.deleteAccount, name='kill-account'),
]

handler404 = 'user.views.custom_404'