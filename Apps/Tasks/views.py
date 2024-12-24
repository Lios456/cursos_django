from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import *

# Create your views here.

def index(request):
    cursos = Curso.objects.all()
    return render(request, 'index.html', {'titulo': 'Cursos disponibles', 'cursos': cursos}) 

"""
  _____                        
 |_   _|_ _ _ __ ___  __ _ ___ 
   | |/ _` | '__/ _ \/ _` / __|
   | | (_| | | |  __/ (_| \__ \
   |_|\__,_|_|  \___|\__,_|___/
                               

"""

@login_required(login_url='/estudiantes/login_user/')
def tareas(request):
    estudiante = Estudiante.objects.prefetch_related('cursos__tarea_set').get(usuario=request.user)
    tareas = Tarea.objects.filter(curso__in=estudiante.cursos.all()).order_by('fecha_entrega')
    return render(request, 'tareas.html', {'titulo': 'Tareas', 'tareas': tareas})



@login_required(login_url='/estudiantes/login_user/')
def tareas_curso(request, c):
    estudiante = Estudiante.objects.get(usuario=request.user)
    tareas = Tarea.objects.filter(curso=c).order_by('fecha_entrega')
    return render(request, 'tareas_curso.html', {'titulo': 'Tareas', 'tareas': tareas})


"""

  __  __       _            _       _           
 |  \/  | __ _| |_ ___ _ __(_) __ _| | ___  ___ 
 | |\/| |/ _` | __/ _ \ '__| |/ _` | |/ _ \/ __|
 | |  | | (_| | ||  __/ |  | | (_| | |  __/\__ \
 |_|  |_|\__,_|\__\___|_|  |_|\__,_|_|\___||___/
                                                

"""

@login_required(login_url='/estudiantes/login_user/')
def materiales(request):
    estudiante = Estudiante.objects.prefetch_related('cursos__recurso_set').get(usuario=request.user)
    materiales = Recurso.objects.filter(curso__in=estudiante.cursos.all()).order_by('fecha_subida')
    return render(request, 'materiales.html', {'titulo': 'Materiales', 'materiales': materiales})

@login_required(login_url='/estudiantes/login_user/')
def materiales_curso(request, c):
    estudiante = Estudiante.objects.get(usuario=request.user)
    cursos = estudiante.cursos.all()
    materiales = Recurso.objects.filter(curso__in=cursos, curso=c)
    return render(request, 'materiales.html', {'titulo': 'Materiales', 'materiales': materiales})

"""
   ____ _                     
  / ___| | __ _ ___  ___  ___ 
 | |   | |/ _` / __|/ _ \/ __|
 | |___| | (_| \__ \  __/\__ \
  \____|_|\__,_|___/\___||___/
                                                                          

"""

@login_required(login_url='/estudiantes/login_user/')
def clases(request):
    estudiante = Estudiante.objects.get(usuario=request.user)
    cursos = estudiante.cursos.all()
    clases = []
    for c in cursos:
        clase = Clase.objects.filter(curso__in=cursos, curso=c)
        clases.append(clase)
    return render(request, 'clases.html', {'titulo': 'Clases', 'clases': clases})

@login_required(login_url='/estudiantes/login_user/')
def clases_curso(request, c):
    estudiante = Estudiante.objects.get(usuario=request.user)
    cursos = estudiante.cursos.all()
    clases = Clase.objects.filter(curso__in=cursos, curso=c)
    return render(request, 'clases_curso.html', {'titulo': 'Clases', 'clases': clases})

"""

   ____                         
  / ___|   _ _ __ ___  ___  ___ 
 | |  | | | | '__/ __|/ _ \/ __|
 | |__| |_| | |  \__ \ (_) \__ \
  \____\__,_|_|  |___/\___/|___/
                                

"""

@login_required(login_url='/estudiantes/login_user/')
def cursos(request):
    estudiante = Estudiante.objects.get(usuario=request.user)
    cursos = estudiante.cursos.all()
    return render(request, 'cursos.html', {'titulo': 'Cursos', 'cursos': cursos})

def ver_curso(request, id):
    curso = Curso.objects.get(id=id)
    return render(request, 'ver_curso.html', {'titulo': 'Curso', 'curso': curso})

#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
