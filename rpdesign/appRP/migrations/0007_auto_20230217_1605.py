# Generated by Django 3.2.16 on 2023-02-17 19:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appRP', '0006_alter_usuario_piso'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='precio_original',
        ),
        migrations.RemoveField(
            model_name='producto',
            name='precio_venta',
        ),
    ]
