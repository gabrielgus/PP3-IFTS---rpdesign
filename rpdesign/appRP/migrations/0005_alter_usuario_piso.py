# Generated by Django 3.2.16 on 2023-02-10 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appRP', '0004_auto_20230206_1240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='piso',
            field=models.CharField(blank=True, default=0, max_length=5),
        ),
    ]
