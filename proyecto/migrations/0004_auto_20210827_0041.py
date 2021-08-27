# Generated by Django 3.2.6 on 2021-08-27 00:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0003_proyecto_estado_de_proyecto'),
    ]

    operations = [
        migrations.AddField(
            model_name='proyecto',
            name='fechaFin',
            field=models.DateField(default=datetime.date(2021, 8, 27), help_text='Fecha estimada de finalización del proyecto'),
        ),
        migrations.AddField(
            model_name='proyecto',
            name='fechaInicio',
            field=models.DateField(default=datetime.date(2021, 8, 27), help_text='Fecha de inicialización del proyecto'),
        ),
    ]
