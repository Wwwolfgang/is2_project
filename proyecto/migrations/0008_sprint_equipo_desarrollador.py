# Generated by Django 3.2.6 on 2021-09-11 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0007_sprint_estado_de_sprint'),
    ]

    operations = [
        migrations.AddField(
            model_name='sprint',
            name='equipo_desarrollador',
            field=models.ManyToManyField(blank=True, to='proyecto.ProyectUser'),
        ),
    ]
