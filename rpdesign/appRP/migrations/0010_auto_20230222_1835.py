# Generated by Django 3.2.16 on 2023-02-22 21:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appRP', '0009_producto_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orden',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creada', models.DateTimeField(auto_now_add=True)),
                ('actualizada', models.DateTimeField(auto_now=True)),
                ('pagada', models.BooleanField(default=False)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-creada'],
            },
        ),
        migrations.CreateModel(
            name='OrdenItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cantidad', models.PositiveIntegerField(default=1)),
                ('orden', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='appRP.orden')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orden_items', to='appRP.producto')),
            ],
        ),
        migrations.DeleteModel(
            name='Carrito',
        ),
        migrations.AddIndex(
            model_name='orden',
            index=models.Index(fields=['-creada'], name='appRP_orden_creada_74999a_idx'),
        ),
    ]
