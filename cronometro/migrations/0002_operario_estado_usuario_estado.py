# Generated by Django 4.2 on 2023-05-08 20:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cronometro', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='operario',
            name='estado',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='usuario',
            name='estado',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
