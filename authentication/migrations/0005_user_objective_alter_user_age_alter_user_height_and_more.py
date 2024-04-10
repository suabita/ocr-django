# Generated by Django 4.2.9 on 2024-04-03 01:45

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_alter_user_physical_activity'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='objective',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Mantener el peso'), (1, 'Perder peso'), (2, 'Ganar peso')], default=0, null=True, verbose_name='objetivo'),
        ),
        migrations.AlterField(
            model_name='user',
            name='age',
            field=models.DecimalField(blank=True, decimal_places=2, default=Decimal('0.0'), max_digits=14, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='edad'),
        ),
        migrations.AlterField(
            model_name='user',
            name='height',
            field=models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)], verbose_name='altura cm'),
        ),
        migrations.AlterField(
            model_name='user',
            name='physical_activity',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Sedentario (poco o nada de ejercicio + trabajo de escritorio)'), (1, 'Ligeramente activo (ejercicio ligero 1-3 días / semana)'), (2, 'Moderadamente activo (ejercicio moderado 3-5 días / semana)'), (3, 'Muy activo (ejercicio pesado 6-7 días / semana)'), (4, 'Extremadamente activo (entrenamiento extenuante 2x / día)')], default=0, null=True, verbose_name='nivel de actividad física'),
        ),
        migrations.AlterField(
            model_name='user',
            name='physiological_state',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Embarazo'), (1, 'Lactancia'), (2, 'No aplica')], default=2, null=True, verbose_name='estado'),
        ),
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(0, 'Female'), (1, 'Male')], default=0, null=True, verbose_name='genero'),
        ),
        migrations.AlterField(
            model_name='user',
            name='weight',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.0'), max_digits=14, validators=[django.core.validators.MinValueValidator(0)], verbose_name='peso kg'),
        ),
    ]
