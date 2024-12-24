from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from ..Estudiantes.views import login_user
urlpatterns = [
    path('', login_user, name='login'),
    path('inicio/', views.index),
    path('cursos/', views.cursos),
    path('ver/curso/<int:id>', views.ver_curso),
    path('tareas/', views.tareas),
    path('clases/<str:c>/', views.clases_curso),
    path('materiales/<str:c>/', views.materiales_curso),
    path('tareas/<str:c>/', views.tareas_curso),
]