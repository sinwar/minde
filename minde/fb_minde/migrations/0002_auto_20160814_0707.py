# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-14 07:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fb_minde', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reminders',
            name='receiverid',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterField(
            model_name='reminders',
            name='remindertime',
            field=models.CharField(max_length=256),
        ),
    ]
