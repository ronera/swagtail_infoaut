# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-05 13:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20170905_1333'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postpagegalleryimage',
            old_name='caption',
            new_name='descrizione',
        ),
    ]