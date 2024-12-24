# Generated by Django 5.1.3 on 2024-12-22 20:56

import Apps.Tasks.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tasks', '0002_rename_nombre_estudiante_usuario_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='clase',
            name='link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='clase',
            name='contenido',
            field=models.FileField(blank=True, null=True, upload_to=Apps.Tasks.models.ruta_clases),
        ),
    ]