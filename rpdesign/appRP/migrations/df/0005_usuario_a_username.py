# Generated by Django 3.2.16 on 2023-02-01 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appRP', '0004_auto_20230201_1310'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario_a',
            name='username',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
