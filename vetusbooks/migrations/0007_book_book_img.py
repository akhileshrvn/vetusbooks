# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-04-10 04:27
from __future__ import unicode_literals

from django.db import migrations, models
import vetusbooks.models


class Migration(migrations.Migration):

    dependencies = [
        ('vetusbooks', '0006_auto_20170409_1133'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='book_img',
            field=models.ImageField(blank=True, null=True, upload_to=vetusbooks.models.get_user_books_path),
        ),
    ]
