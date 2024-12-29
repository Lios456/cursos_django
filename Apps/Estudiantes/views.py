from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from ..Tasks.models import *
# Create your views here.

def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Bienvenido {}".format(username))
            return redirect('/inicio/')
        else:
            messages.error(request, "Usuario o contraseña incorrectos")
            return redirect('/estudiantes/login_user/')
    else:
        return render(request, 'authenticate/login.html', {'titulo': 'Inicio de Sesión'})


def logout_user(request):
    logout(request)
    messages.success(request, f"Sesión cerrada exitosamente, nos vemos pronto ")
    return redirect('/inicio/')

def registro_usuario(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            grupo = Group.objects.get(name='estudiantes')
            user.groups.add(grupo)
            estudiante = Estudiante()
            estudiante.usuario = user
            estudiante.save()
            messages.info(request, "Estudiante registrado exitosamente\nPor favor inicia sesión y No olvides tu contraseña")
            return redirect('/estudiantes/login_user/')
        else:
            usuario = User.objects.filter(username=request.POST.get('username'))
            if usuario:
                messages.error(request, "El usuario ya existe, por favor intenta con otro")
            messages.error(request, "Error al registrar el usuario, por favor verifica los datos e intentalo de nuevo")
            return redirect('/estudiantes/registrar_usuario/')
    else:
        form = UserCreationForm()
        return render(request, 'authenticate/registro.html', {'titulo': 'Registro de Usuario', 'form': form})

@login_required(login_url='/estudiantes/login_user/')
def perfil(request):
    return render(request, 'perfil.html', {'titulo': 'Perfil de Usuario'})

@login_required(login_url='/estudiantes/login_user/')
def inscribirse(request, id):
    estudiante = Estudiante.objects.get(usuario=request.user)
    estudiante.cursos.add(id)
    messages.success(request, f"Inscripción en {Curso.objects.get(id=id)} exitosa")
    return redirect('/inicio/')

@login_required(login_url='/estudiantes/login_user/')
def comentar(request):
    if request.method == "POST":
        Comentario.objects.create(
            tarea = Tarea.objects.get(id=request.POST.get('tx_tarea')),
            estudiante=Estudiante.objects.get(usuario=request.user),
            contenido=request.POST.get('tx_contenido')
        )
        messages.success(request, "Comentario enviado exitosamente")
    return redirect(f'/tarea/{request.POST.get("tx_tarea")}')
