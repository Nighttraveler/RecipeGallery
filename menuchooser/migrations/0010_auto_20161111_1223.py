# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-11 15:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menuchooser', '0009_menumodel_public_or_private'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menumodel',
            old_name='public_or_private',
            new_name='publica',
        ),
    ]
