# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-05 17:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0010_auto_20171104_1728'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subtopic',
            options={'ordering': ['chapter', 'subtopic_serial']},
        ),
    ]
