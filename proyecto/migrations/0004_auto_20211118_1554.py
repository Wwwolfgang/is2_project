# Generated by Django 3.2.6 on 2021-11-18 19:54

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0003_auto_20211028_2347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daily',
            name='duracion',
            field=models.DecimalField(decimal_places=2, help_text='Trabajo realizado en horas.', max_digits=4, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='proyectuser',
            name='horas_diarias',
            field=models.DecimalField(decimal_places=2, help_text='La cantidad de horas que trabaja el desarrollador por día.', max_digits=4, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='userstory',
            name='tiempo_estimado_dev',
            field=models.PositiveIntegerField(blank=True, default=0, help_text='Tiempo de duración estimado por el desarrollador asignado.', null=True, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='userstory',
            name='tiempo_estimado_scrum_master',
            field=models.PositiveIntegerField(blank=True, default=0, help_text='Tiempo de duración estimado por el scrum master.', null=True, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
