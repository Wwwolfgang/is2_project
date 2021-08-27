# Generated by Django 3.2.6 on 2021-08-27 00:45

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0004_auto_20210827_0041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyecto',
            name='fechaFin',
            field=models.DateField(default=datetime.datetime(2021, 8, 27, 0, 45, 36, 452824, tzinfo=utc), help_text='Fecha estimada de finalización del proyecto'),
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='fechaInicio',
            field=models.DateField(default=datetime.datetime(2021, 8, 27, 0, 45, 36, 452792, tzinfo=utc), help_text='Fecha de inicialización del proyecto'),
        ),
    ]
