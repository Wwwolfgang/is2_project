# Generated by Django 3.2.6 on 2021-09-17 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('proyecto', '0016_userstory_product_backlog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstory',
            name='descripcion',
            field=models.TextField(blank=True, verbose_name='Descripción del user story'),
        ),
    ]
