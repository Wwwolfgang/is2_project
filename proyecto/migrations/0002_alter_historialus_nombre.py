# Generated by Django 3.2.6 on 2021-10-11 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historialus',
            name='nombre',
            field=models.CharField(max_length=100, verbose_name='Nombre del user story'),
        ),
    ]
