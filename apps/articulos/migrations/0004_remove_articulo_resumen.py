# Generated by Django 5.0 on 2023-12-26 23:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articulos', '0003_alter_articulo_resumen'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articulo',
            name='resumen',
        ),
    ]
