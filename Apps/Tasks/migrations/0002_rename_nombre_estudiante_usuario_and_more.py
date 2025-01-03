# Generated by Django 5.1.3 on 2024-12-22 20:51

import Apps.Tasks.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tasks', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='estudiante',
            old_name='nombre',
            new_name='usuario',
        ),
        migrations.RemoveField(
            model_name='estudiante',
            name='contrasenia',
        ),
        migrations.AlterField(
            model_name='clase',
            name='contenido',
            field=models.FileField(upload_to=Apps.Tasks.models.ruta_clases),
        ),
        migrations.AlterField(
            model_name='estudiante',
            name='cursos',
            field=models.ManyToManyField(to='Tasks.curso'),
        ),
        migrations.AlterField(
            model_name='recurso',
            name='archivos',
            field=models.FileField(upload_to=Apps.Tasks.models.ruta_recursos),
        ),
        migrations.AlterField(
            model_name='tarea',
            name='archivo',
            field=models.FileField(upload_to=Apps.Tasks.models.ruta_tareas),
        ),
    ]
