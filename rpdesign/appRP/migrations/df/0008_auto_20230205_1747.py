# Generated by Django 3.2.16 on 2023-02-05 20:47

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appRP', '0007_auto_20230202_1140'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='cantidad',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='producto',
            name='creado_el',
            field=models.DateTimeField(auto_now_add=True, default=datetime.date.today),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='producto',
            name='precio_original',
            field=models.FloatField(default=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='producto',
            name='precio_venta',
            field=models.FloatField(default=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='producto',
            name='status',
            field=models.BooleanField(default=False, help_text='0-mostrar,1-ocultar'),
        ),
        migrations.CreateModel(
            name='Carrito',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('producto_qty', models.IntegerField()),
                ('creado_el', models.DateTimeField(auto_now_add=True)),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appRP.producto')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
