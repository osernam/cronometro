# Generated by Django 4.1.5 on 2023-09-04 17:21

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Maquina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=50)),
                ('estado', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Operacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=50)),
                ('estado', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Operario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('entidad', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('estado', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('clave', models.CharField(max_length=254)),
                ('rol', models.CharField(choices=[('A', 'Administrador'), ('U', 'Usuario')], default='U', max_length=20)),
                ('fecha_nacimiento', models.DateField(default=datetime.date.today)),
                ('estado', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='OperacionOperario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechas', models.DateTimeField(auto_now_add=True)),
                ('tiempoEstandar', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('factorRitmo', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('escalaSuplementos', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('estado', models.BooleanField(default=True)),
                ('idMaquinas', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cronometro.maquina')),
                ('idOperacion', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cronometro.operacion')),
                ('idOperario', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cronometro.operario')),
            ],
        ),
    ]
