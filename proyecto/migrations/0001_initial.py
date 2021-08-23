# Generated by Django 3.2.6 on 2021-08-23 16:42

import datetime
import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='burnDownChart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='comentario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codComentario', models.CharField(max_length=50)),
                ('codUserStory', models.CharField(max_length=50)),
                ('codProyecto', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=50)),
                ('fecha', models.DateField(verbose_name=datetime.date(2021, 8, 23))),
            ],
        ),
        migrations.CreateModel(
            name='historialCambiosUS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Permiso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
            options={
                'verbose_name_plural': 'permisos',
            },
        ),
        migrations.CreateModel(
            name='rol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='usuarioProyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='userStory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreUserStory', models.CharField(max_length=50)),
                ('codigoUserStory', models.CharField(max_length=50)),
                ('listaParticipantes', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), max_length=10, size=None)),
                ('descripcionUserStory', models.CharField(max_length=50)),
                ('estado', models.CharField(max_length=10)),
                ('estimacion', models.IntegerField()),
                ('tiempoEmpleado', models.IntegerField()),
                ('comentarios', models.ManyToManyField(related_name='comentario', to='proyecto.comentario')),
            ],
        ),
        migrations.CreateModel(
            name='sprint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreSprint', models.CharField(max_length=50)),
                ('codSprint', models.CharField(max_length=50)),
                ('nroUserStories', models.IntegerField()),
                ('fechaInicio', models.DateField()),
                ('fechaFin', models.DateField()),
                ('listaStories', models.ManyToManyField(max_length=100, to='proyecto.userStory')),
            ],
        ),
        migrations.CreateModel(
            name='RolSistema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Define el nombre del Rol de sistema', max_length=50, verbose_name='Nombre del Rol')),
                ('permisos', models.ManyToManyField(to='proyecto.Permiso')),
            ],
            options={
                'verbose_name_plural': 'system_roles',
            },
        ),
    ]
