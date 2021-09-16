# Generated by Django 3.2.6 on 2021-09-13 23:14

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0018_auto_20210909_2216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyecto',
            name='fechaFin',
            field=models.DateField(default=datetime.datetime(2021, 9, 13, 23, 14, 39, 159847, tzinfo=utc), help_text='Fecha estimada de finalización del proyecto'),
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='fechaInicio',
            field=models.DateField(default=datetime.datetime(2021, 9, 13, 23, 14, 39, 159797, tzinfo=utc), help_text='Fecha de inicialización del proyecto'),
        ),
    ]
