from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
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
    return render(request, 'tareas_curso.html', {'titulo': 'Tareas', 
                                                 'tareas': tareas
                                                 })

@login_required(login_url='/estudiantes/login_user/')
def ver_tarea(request, id):
    tarea = Tarea.objects.get(id=id)
    comentarios = Comentario.objects.filter(tarea=tarea)
    return render(request, 'tarea.html', {'titulo': 'Tarea', 't': tarea,'comentarios': comentarios})

@login_required(login_url='/estudiantes/login_user/')
def completar_tarea(request, id):
    if request.method == 'POST':
        tarea = Tarea.objects.get(id=id)
        tarea.completada = True
        tarea.save()
        messages.success(request, 'Tarea marcada como completa')
        return redirect(f'/tarea/{id}')
    else:
        return redirect('/tareas/')
    
@login_required(login_url='/estudiantes/login_user/')
@user_passes_test(lambda u: u.is_superuser, login_url='/estudiantes/login_user/')
def administrar_tareas(request):
    if request.method == 'POST':
        try:
            Tarea.objects.create(
                titulo=request.POST['tx_titulo'],
                descripcion=request.POST['tx_descripcion'], 
                fecha_entrega=request.POST['tx_f_entrega'],
                curso= Curso.objects.get(id=request.POST['tx_curso']),
                archivo=request.FILES.get('tx_archivo'),
                fecha_inicio = request.POST['tx_f_inicio']
            )
            messages.success(request, 'Tarea agregada correctamente')
        except Exception as e:
            messages.error(request, f"Hubo un error: {e}")
        return render(request, 'administrar_tarea.html', 
                      {'titulo': 'Administración de tareas',
                       'tareas': Tarea.objects.all(),
                       'cursos': Curso.objects.all()})
    else:
        return render(request, 'administrar_tarea.html', 
                      {'titulo': 'Administración de tareas',
                       'tareas': Tarea.objects.all(),
                       'cursos': Curso.objects.all()})
    
@login_required(login_url='/estudiantes/login_user/')
@user_passes_test(lambda u: u.is_superuser, login_url='/estudiantes/login_user/')   
def eliminar_tarea(request, id):
    if request.method == 'POST':
        try:
            Tarea.objects.get(id=id).delete()
            messages.success(request, 'Tarea eliminada')
        except Exception as e:
            messages.error(request, f"Hubo un error al eliminar la tarea, Intentalo de nuevo\n{e}")
        return redirect('/administrar/tareas/')
    else:
        return redirect('/administrar/tareas/')
    
@login_required(login_url='/estudiantes/login_user/')
@user_passes_test(lambda u: u.is_superuser, login_url='/estudiantes/login_user/')   
def editar_tarea(request, id):
    tarea = Tarea.objects.get(id=id)
    if request.method == 'POST':
        try:
            tarea.titulo = request.POST['tx_titulo']
            tarea.descripcion = request.POST['tx_descripcion']
            tarea.fecha_inicio = request.POST['tx_f_inicio']
            tarea.fecha_entrega = request.POST['tx_f_entrega']
            tarea.curso = Curso.objects.get(id=request.POST['tx_curso'])
            tarea.archivo = request.FILES.get('tx_archivo') if request.FILES.get('tx_archivo') else tarea.archivo
            tarea.save()
            messages.success(request, 'Tarea actualizada')
            return redirect('/administrar/tareas/')
        except Exception as e:
            messages.error(request, f'Hubo un problema: {str(e)}')
            return render(request, 'administrar_tarea.html', 
                      {'titulo': 'Editar tareas',
                       'tareas': Tarea.objects.all(),
                       'cursos': Curso.objects.all(),
                       't': tarea
                       })
    else:
        messages.warning(request, 'Edita con cuidado las Tareas que ya han sido asignadas a los estudiantes')
        return render(request, 'administrar_tarea.html', 
                      {'titulo': 'Editar tareas',
                       'tareas': Tarea.objects.all(),
                       'cursos': Curso.objects.all(),
                       't': tarea
                       })


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
    return render(request, 'materiales.html', {'titulo': 'Materiales', 'materiales': materiales, 'estudiante':estudiante})

@login_required(login_url='/estudiantes/login_user/')
def materiales_curso(request, c):
    estudiante = Estudiante.objects.get(usuario=request.user)
    cursos = estudiante.cursos.all()
    materiales = Recurso.objects.filter(curso__in=cursos, curso=c)
    return render(request, 'materiales.html', {'titulo': 'Materiales', 'materiales': materiales})

@login_required(login_url='/estudiantes/login_user/')
@user_passes_test(lambda u: u.is_superuser, login_url='/estudiantes/login_user/')
def administrar_materiales(request):
    if request.method == 'POST':
        try:
            Recurso.objects.create(
            titulo=request.POST['tx_titulo'],
            descripcion=request.POST['tx_descripcion'],
            curso=Curso.objects.get(id=request.POST['tx_curso']),
            link=request.POST['tx_link'],
            archivos = request.FILES.get('tx_archivos')
            )
            messages.success(request, 'Material agregado')
        except Exception as e:
            messages.error(request, f"Hubo un error al agregar el recurso, Intentalo de nuevo\n{e}")
        return redirect('/materiales/')
    else:
        cursos = Curso.objects.all()
        materiales = Recurso.objects.all()
        return render(request, 'administrar_material.html', 
                      {'titulo': 'Administración de materiales', 
                       'cursos': cursos,
                       'materiales': materiales})
    
@login_required(login_url='/estudiantes/login_user/')
@user_passes_test(lambda u: u.is_superuser, login_url='/estudiantes/login_user/')   
def eliminar_material(request, id):
    try:
        Recurso.objects.get(id=id).delete()
        messages.success(request, 'Material eliminado')
    except Exception as e:
        messages.error(request, f"Hubo un error al eliminar el Material, Intentalo de nuevo\n{e}")
    return redirect('/administrar/materiales/')

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
    try:
        estudiante = Estudiante.objects.get(usuario=request.user)
        cursos = estudiante.cursos.all()
        return render(request, 'cursos.html', {'titulo': 'Cursos', 'cursos': cursos})
    except Exception as e:
        messages.error(request, f"{e}")
        return redirect('/inicio/')

@login_required(login_url='/estudiantes/login_user/')
@user_passes_test(lambda u: u.is_superuser, login_url='/estudiantes/login_user/')
def agregar_curso(request):
    if request.method == 'POST':
        Curso.objects.acreate(
            nombre=request.POST['tx_nombre'],
            imagen=request.FILES['tx_imagen'], 
            descripcion=request.POST['tx_descripcion'],
            f_inicio=request.POST['tx_f_inicio'],
            f_fin=request.POST['tx_f_fin']
            )
        messages.success(request, 'Curso agregado')
        return redirect('/cursos/')
    else:
        return render(request, 'agregar_curso.html', {'titulo': 'Agregar curso'})

def ver_curso(request, id):
    curso = Curso.objects.get(id=id)
    return render(request, 'ver_curso.html', {'titulo': 'Curso', 'curso': curso})

@login_required(login_url='/estudiantes/login_user/')
@user_passes_test(lambda u: u.is_superuser, login_url='/estudiantes/login_user/')
def administrar_cursos(request):
    if request.method == 'POST':
        try:
            Curso.objects.update_or_create(
                nombre=request.POST['tx_nombre'],
                imagen=request.FILES.get('tx_imagen') if request.FILES.get('tx_imagen') else 'cursos/default.png', 
                descripcion=request.POST['tx_descripcion'],
                f_inicio=request.POST['tx_f_inicio'],
                f_fin=request.POST['tx_f_fin']
            )
            messages.success(request, 'Curso agregado correctamente')
        except Exception as e:
            messages.error(request, f"Hubo un error al agregar el Curso, Intentalo de nuevo\n{e}")
        return render(request, 'administrar_curso.html', 
                      {'titulo': 'Administración de cursos',
                       'cursos': Curso.objects.all()})
    else:
        return render(request, 'administrar_curso.html', 
                      {'titulo': 'Administración de cursos',
                       'cursos': Curso.objects.all()})

@login_required(login_url='/estudiantes/login_user/')
@user_passes_test(lambda u: u.is_superuser, login_url='/estudiantes/login_user/')   
def eliminar_curso(request, id):
    try:
        Curso.objects.get(id=id).delete()
        messages.success(request, 'Curso eliminado')
    except Exception as e:
        messages.error(request, f"Hubo un error al eliminar el Curso, Intentalo de nuevo\n{e}")
    return redirect('/administrar/cursos/')

@login_required(login_url='/estudiantes/login_user/')
@user_passes_test(lambda u: u.is_superuser, login_url='/estudiantes/login_user/')   
def editar_curso(request, id):
    curso = Curso.objects.get(id=id)
    if request.method == "POST":
        try:
            curso.nombre = request.POST['tx_nombre']
            curso.imagen = request.FILES.get('tx_imagen') if request.FILES.get('tx_imagen') else curso.imagen
            curso.descripcion = request.POST['tx_descripcion']
            curso.f_inicio = request.POST['tx_f_inicio']
            curso.f_fin = request.POST['tx_f_fin']
            curso.save()
            messages.success(request, 'Curso actualizado')
        except Exception as e:
            messages.error(request, f"Hubo un error al editar el Curso, Intentalo de nuevo\n{e}")
        return redirect('/administrar/cursos/')
    else:
        
        messages.warning(request, 'Edita con cuidado los cursos que ya han sido asignados a los estudiantes')
        return render(request, 'administrar_curso.html', 
                      {'titulo': 'Editar curso',
                        'c': curso,
                        'cursos': Curso.objects.all()
                        })

