# Generated by Django 3.2.16 on 2023-02-20 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appRP', '0007_auto_20230217_1605'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='is_admin',
            field=models.BooleanField(default=False, help_text='Designa si un usuario es Administrador del sitio.', verbose_name='Es Administrador?'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='status',
            field=models.BooleanField(default=False, help_text='1-mostrar,0-ocultar'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='dni',
            field=models.PositiveIntegerField(default=0, unique=True, verbose_name='Nro. de Documento'),
        ),
    ]
