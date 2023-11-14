# Generated by Django 4.2 on 2023-10-31 21:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cronometro', '0006_empresa_maquina_empresa_operacion_empresa_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='maquina',
            name='empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cronometro.empresa'),
        ),
        migrations.AlterField(
            model_name='operacion',
            name='empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cronometro.empresa'),
        ),
        migrations.AlterField(
            model_name='operario',
            name='empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cronometro.empresa'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='cronometro.empresa'),
        ),
    ]
