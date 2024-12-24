from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login_user/', views.login_user ),
    path('logout_user/', views.logout_user),
    path('registrar_usuario/', views.registro_usuario),
    path('ver_perfil/', views.perfil),
    path('inscribirse/<int:id>/', views.inscribirse),
    
]