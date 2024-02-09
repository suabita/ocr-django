# Generated by Django 4.2.9 on 2024-02-07 04:16

import customized.mixin
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('name', models.CharField(db_index=True, max_length=100, unique=True, verbose_name='Unit name')),
            ],
            options={
                'verbose_name': 'Unit',
                'verbose_name_plural': 'Units',
            },
            bases=(customized.mixin.SlugModelMixin, models.Model),
        ),
    ]
