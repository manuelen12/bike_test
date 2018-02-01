# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-02-01 10:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'bike',
            },
        ),
        migrations.CreateModel(
            name='PriceByFrecuency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('frequently', models.SmallIntegerField(choices=[(2, 'Daily'), (3, 'weekly'), (1, 'Hourly')], default=1)),
                ('price', models.IntegerField()),
            ],
            options={
                'db_table': 'price_by_frecuency',
            },
        ),
        migrations.CreateModel(
            name='Rent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.IntegerField()),
                ('status', models.BooleanField(default=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rent_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'rent',
            },
        ),
        migrations.AddField(
            model_name='bike',
            name='price_by_frecuency',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rents.PriceByFrecuency'),
        ),
        migrations.AddField(
            model_name='bike',
            name='rent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rents.Rent'),
        ),
    ]