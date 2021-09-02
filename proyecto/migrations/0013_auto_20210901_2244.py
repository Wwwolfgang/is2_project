# Generated by Django 3.2.6 on 2021-09-01 22:44

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0012_auto_20210901_0208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proyecto',
            name='fechaFin',
            field=models.DateField(default=datetime.datetime(2021, 9, 1, 22, 44, 36, 654329, tzinfo=utc), help_text='Fecha estimada de finalización del proyecto'),
        ),
        migrations.AlterField(
            model_name='proyecto',
            name='fechaInicio',
            field=models.DateField(default=datetime.datetime(2021, 9, 1, 22, 44, 36, 654295, tzinfo=utc), help_text='Fecha de inicialización del proyecto'),
        ),
        migrations.AlterField(
            model_name='rolproyecto',
            name='nombre',
            field=models.CharField(max_length=60, verbose_name='Nombre del rol'),
        ),
    ]