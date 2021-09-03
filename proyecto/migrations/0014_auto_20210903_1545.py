# Generated by Django 3.2.6 on 2021-09-03 15:45

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0013_auto_20210901_2244'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyecto',
            name='estado_de_proyecto',
            field=models.CharField(choices=[('A', 'Activo'), ('I', 'Inicializado'), ('C', 'Cancelado'), ('F', 'Finalizado')], default='I', max_length=1),
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='fechaFin',
            field=models.DateField(default=datetime.datetime(2021, 9, 3, 15, 45, 58, 394241, tzinfo=utc), help_text='Fecha estimada de finalización del proyecto'),
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='fechaInicio',
            field=models.DateField(default=datetime.datetime(2021, 9, 3, 15, 45, 58, 394200, tzinfo=utc), help_text='Fecha de inicialización del proyecto'),
        ),
    ]
