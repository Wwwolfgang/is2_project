# Generated by Django 3.2.6 on 2021-09-01 02:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sso', '0002_alter_user_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': [('p_is_user', 'El usuario es un usuario registrado que se le asignó un rol. Con este permiso tiene la posibilidad de ver más en el sistema.'), ('p_puede_crear_proyecto', 'El usuario puede crear nuevos proyectos.')], 'verbose_name_plural': 'users'},
        ),
    ]