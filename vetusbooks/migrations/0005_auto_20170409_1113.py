# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-04-09 05:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vetusbooks', '0004_auto_20170409_1040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='pic_folder/None/no-img.jpg', upload_to='media/'),
        ),
    ]
