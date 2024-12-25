from django.db import models
from django import forms
from django.contrib.auth.models import User

# Función para generar la ruta de subida
def ruta_recursos(instance, filename):
    return f'{instance.curso.nombre}/recursos/{filename}'

def ruta_clases(instance, filename):
    return f'{instance.curso.nombre}/clases/{filename}'

def ruta_tareas(instance, filename):
    return f'{instance.curso.nombre}/tareas/{filename}'

class Curso(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='cursos/', blank=True, null=True, default='cursos/default.png')
    descripcion = models.TextField()
    f_inicio = models.DateField(blank=True, null=True)
    f_fin = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return f"CURSO: {self.nombre}"

class Estudiante(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    cursos = models.ManyToManyField(Curso)
    
    def __str__(self):
        return f"ESTUDIANTE: {self.usuario.username}"
    
class Clase(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    contenido = models.FileField(upload_to=ruta_clases, blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return f"CLASE: {self.nombre}"
    
class Recurso(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    archivos = models.FileField(upload_to=ruta_recursos, blank=True, null=True)
    fecha_subida = models.DateField(auto_now_add=True)
    link = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return f"RECURSO: {self.titulo}"

    
class Tarea(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_entrega = models.DateField()
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    archivo = models.FileField(upload_to=ruta_tareas, blank=True, null=True)
    estado = models.BooleanField(default=False)
    fecha_inicio = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"TAREA: {self.titulo}"
    
class Comentario(models.Model):
    id = models.AutoField(primary_key=True)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    tarea = models.ForeignKey('Tarea', on_delete=models.CASCADE)
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    oculto = models.BooleanField(default=False)
    
    def __str__(self):
        return f"COMENTARIO: {self.contenido} de {self.estudiante}"
