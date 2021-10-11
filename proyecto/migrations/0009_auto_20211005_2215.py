# Generated by Django 3.2.6 on 2021-10-05 22:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0008_alter_userstory_nombre'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='proyecto',
            options={'permissions': (('p_acceder_proyectos', 'Permiso de acceder proyecto.'), ('p_cancelar_proyectos', 'Permiso de cancelar proyecto.'), ('p_editar_proyectos', 'Permiso de editar proyecto.'), ('p_finalizar_proyectos', 'Permiso de finalizar proyecto.'), ('p_administrar_participantes', 'Permiso para agregar y eliminar participantes del proyecto.'), ('p_administrar_roles', 'Permite que el usuario pueda agregar, editar, importar y eliminar roles del proyecto. Solo los permisos del scrum master no se podrán modificar.'), ('p_administrar_sprint', 'Permite que el usuario pueda gestionar los parámetros de los sprints, así como planificarlos, iniciarlos y finalizarlos.'), ('p_administrar_us', 'Permite que el usuario pueda agregar, editar y eliminar los user stories del proyecto.'))},
        ),
        migrations.AlterModelOptions(
            name='rolproyecto',
            options={},
        ),
    ]