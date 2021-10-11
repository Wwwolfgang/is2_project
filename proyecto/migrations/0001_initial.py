# Generated by Django 3.2.6 on 2021-10-11 15:14

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductBacklog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreProyecto', models.CharField(max_length=50)),
                ('fechaInicio', models.DateField(default=datetime.datetime.now, help_text='Fecha de inicialización del proyecto')),
                ('fechaFin', models.DateField(default=datetime.datetime.now, help_text='Fecha estimada de finalización del proyecto')),
                ('estado_de_proyecto', models.CharField(choices=[('A', 'Activo'), ('I', 'Inicializado'), ('C', 'Cancelado'), ('F', 'Finalizado')], default='I', max_length=1)),
                ('equipo', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('p_acceder_proyectos', 'Permiso de acceder proyecto.'), ('p_cancelar_proyectos', 'Permiso de cancelar proyecto.'), ('p_editar_proyectos', 'Permiso de editar proyecto.'), ('p_finalizar_proyectos', 'Permiso de finalizar proyecto.'), ('p_administrar_participantes', 'Permiso para agregar y eliminar participantes del proyecto.'), ('p_administrar_roles', 'Permite que el usuario pueda agregar, editar, importar y eliminar roles del proyecto. Solo los permisos del scrum master no se podrán modificar.'), ('p_administrar_sprint', 'Permite que el usuario pueda gestionar los parámetros de los sprints, así como planificarlos, iniciarlos y finalizarlos.'), ('p_administrar_us', 'Permite que el usuario pueda editar los user stories del proyecto (cambiar estado, nombre, descripción y horas).'), ('p_eliminar_us', 'Permite que el usuario pueda eliminar user stories del proyecto (cambiar estado, nombre, descripción y horas).'), ('p_administrar_us_qa', 'Con este permiso el usuario puede cambiar el estado de un user story a QA. Inicialmente es un permiso reservado al scrum master.'), ('p_aprobar_us', 'Con este permiso el usuario puede agregar un user story en estado no aprobado, así como también modificarlo y aprobarlo para que pase al product backlog.'), ('p_eliminar_daily', 'Permite que el usuario pueda eliminar el daily asociado a un user story.'), ('p_administrar_devs', 'Con este permiso el usuario puede gestionar los desarrolladores en un sprint.')),
            },
        ),
        migrations.CreateModel(
            name='ProyectUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('horas_diarias', models.DecimalField(decimal_places=2, help_text='La cantidad de horas que trabaja el desarrollador por día.', max_digits=4)),
            ],
        ),
        migrations.CreateModel(
            name='Sprint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identificador', models.CharField(default='Sprint', max_length=50)),
                ('fechaInicio', models.DateField(null=True)),
                ('fechaFin', models.DateField(help_text='Fecha estimada de finalización del Sprint. Dependiendo de esta fecha se mostrarán alertas.', null=True)),
                ('duracionSprint', models.IntegerField(default=14, help_text='Duración estimada en días', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(60)])),
                ('estado_de_sprint', models.CharField(choices=[('A', 'Activo'), ('I', 'Inicializado'), ('C', 'Cancelado'), ('F', 'Finalizado')], default='I', max_length=1)),
                ('carga_horaria', models.DecimalField(blank=True, decimal_places=2, default=0, help_text='Total de horas de todos los user storys asignados', max_digits=8, null=True)),
                ('horas_disponibles', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=8, null=True)),
                ('proyecto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='proyecto.proyecto')),
            ],
        ),
        migrations.CreateModel(
            name='UserStory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre del user story')),
                ('descripcion', models.TextField(blank=True, verbose_name='Descripción del user story')),
                ('tiempo_estimado_scrum_master', models.PositiveIntegerField(blank=True, default=0, help_text='Tiempo de duración estimado por el scrum master.', null=True)),
                ('tiempo_estimado_dev', models.PositiveIntegerField(blank=True, default=0, help_text='Tiempo de duración estimado por el desarrollador asignado.', null=True)),
                ('tiempo_promedio_calculado', models.DecimalField(blank=True, decimal_places=2, help_text='Tiempo de duración promedio entre los dos tiempos estimados.', max_digits=4, null=True)),
                ('prioridad_user_story', models.CharField(choices=[('B', 'Baja'), ('A', 'Alta'), ('M', 'Media'), ('E', 'Emergencia')], default='B', max_length=1)),
                ('estado_aprobacion', models.CharField(choices=[('T', 'Temporal'), ('A', 'Aprobado'), ('C', 'Cancelado')], default='T', max_length=1)),
                ('estado_user_story', models.CharField(choices=[('TD', 'To do'), ('DG', 'Doing'), ('DN', 'Done'), ('QA', 'Quality Assurance')], default='TD', max_length=2)),
                ('last_estimated', models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True)),
                ('creador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('encargado', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proyecto.proyectuser')),
                ('product_backlog', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proyecto.productbacklog')),
                ('sprint', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proyecto.sprint')),
            ],
            options={
                'permissions': (('us_manipular_userstory_dailys', 'Permiso de manipular los dailys de un userstory.'),),
            },
        ),
        migrations.CreateModel(
            name='RolProyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=60, verbose_name='Nombre del rol')),
                ('participantes', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
                ('permisos', models.ManyToManyField(to='auth.Permission')),
                ('proyecto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proyecto.proyecto')),
            ],
        ),
        migrations.AddField(
            model_name='proyectuser',
            name='sprint',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sprint_team', to='proyecto.sprint'),
        ),
        migrations.AddField(
            model_name='proyectuser',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='proyecto',
            name='equipo_desarrollador',
            field=models.ManyToManyField(blank=True, to='proyecto.ProyectUser'),
        ),
        migrations.AddField(
            model_name='proyecto',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='creador', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='productbacklog',
            name='proyecto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyecto.proyecto'),
        ),
        migrations.CreateModel(
            name='HistorialUS',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20, verbose_name='Nombre del user story')),
                ('descripcion', models.TextField(blank=True, verbose_name='Descripción del user story')),
                ('version', models.IntegerField()),
                ('prioridad', models.CharField(choices=[('B', 'Baja'), ('A', 'Alta'), ('M', 'Media'), ('E', 'Emergencia')], default='B', max_length=1)),
                ('us_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='proyecto.userstory')),
            ],
        ),
        migrations.CreateModel(
            name='Daily',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('duracion', models.DecimalField(decimal_places=2, help_text='Trabajo realizado en horas.', max_digits=4)),
                ('impedimiento_comentario', models.TextField(blank=True, verbose_name='Descripcion de las dificultades encontradas durante el desarrollo')),
                ('progreso_comentario', models.TextField(blank=True, verbose_name='Descripcion de los progresos encontrados durante el desarrollo')),
                ('fecha', models.DateField(blank=True, null=True)),
                ('sprint', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proyecto.sprint')),
                ('user_story', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='proyecto.userstory')),
            ],
        ),
    ]
