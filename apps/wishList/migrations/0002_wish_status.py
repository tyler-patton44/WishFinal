# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-10-22 16:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wishList', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wish',
            name='status',
            field=models.CharField(default='pending', max_length=255),
        ),
    ]
