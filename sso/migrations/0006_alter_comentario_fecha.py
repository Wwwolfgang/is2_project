# Generated by Django 3.2.6 on 2021-08-20 20:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sso', '0005_auto_20210818_0031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='fecha',
            field=models.DateField(verbose_name=datetime.date(2021, 8, 20)),
        ),
    ]
