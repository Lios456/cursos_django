from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from ..Estudiantes.views import login_user
urlpatterns = [
    path('', login_user, name='login'),
    path('inicio/', views.index),

    path('cursos/', views.cursos),
    path('ver/curso/<int:id>', views.ver_curso),
    path('administrar/cursos/', views.administrar_cursos),
    path('administrar/cursos/eliminar/<int:id>', views.eliminar_curso),
    path('administrar/cursos/editar/<int:id>', views.editar_curso),

    path('tareas/', views.tareas),
    path('tarea/<int:id>', views.ver_tarea),
    path('tareas/<str:c>/', views.tareas_curso),
    path('administrar/tareas/', views.administrar_tareas),
    path('completar_tarea/<int:id>', views.completar_tarea),
    path('administrar/tareas/eliminar/<int:id>', views.eliminar_tarea),
    path('administrar/tareas/editar/<int:id>', views.editar_tarea),

    path('clases/<str:c>/', views.clases_curso),

    path('materiales/<str:c>/', views.materiales_curso),
    path('materiales/', views.materiales),
    path('administrar/materiales/', views.administrar_materiales),
    path('administrar/materiales/eliminar/<int:id>', views.eliminar_material),
    path('administrar/materiales/editar/<int:id>', views.editar_material),
    
]