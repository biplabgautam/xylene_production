# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-05 17:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tempcms', '0009_auto_20171105_2236'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tempnumerical',
            options={'ordering': ['chapter', '-date_modified']},
        ),
        migrations.AlterModelOptions(
            name='tempsaq',
            options={'ordering': ['chapter', '-date_modified']},
        ),
        migrations.AlterModelOptions(
            name='tempsubsectionimage',
            options={'ordering': ['subsection', '-date_modified']},
        ),
    ]