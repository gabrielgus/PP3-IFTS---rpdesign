# Generated by Django 3.2.16 on 2023-02-06 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appRP', '0008_auto_20230205_1747'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='altura',
            field=models.IntegerField(blank=True, default=' '),
        ),
        migrations.AddField(
            model_name='usuario',
            name='calle',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='usuario',
            name='cod_postal',
            field=models.CharField(blank=True, default='', max_length=255, verbose_name='Codigo Postal'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='depto',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='usuario',
            name='localidad',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='usuario',
            name='piso',
            field=models.IntegerField(blank=True, default=' '),
        ),
    ]