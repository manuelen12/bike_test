# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-02-01 12:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='city',
            name='state',
        ),
        migrations.DeleteModel(
            name='Size',
        ),
        migrations.RemoveField(
            model_name='state',
            name='country',
        ),
        migrations.DeleteModel(
            name='TimeZone',
        ),
        migrations.DeleteModel(
            name='City',
        ),
        migrations.DeleteModel(
            name='Country',
        ),
        migrations.DeleteModel(
            name='State',
        ),
    ]