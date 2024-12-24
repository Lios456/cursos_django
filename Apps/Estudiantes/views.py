from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
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
            grupo = Group.objects.get(name='Estudiantes')  # Asegúrate de que el grupo 'Estudiantes' exista
            user.groups.add(grupo)
            
            messages.success(request, "Estudiante registrado exitosamente")
            messages.info(request, "Por favor inicia sesión y No olvides tu contraseña")
            return redirect('/estudiantes/login_user/')
        pass
    else:
        form = UserCreationForm()
        return render(request, 'authenticate/registro.html', {'titulo': 'Registro de Usuario', 'form': form})
