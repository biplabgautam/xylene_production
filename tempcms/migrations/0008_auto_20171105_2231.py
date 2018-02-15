# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-05 16:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tempcms', '0007_auto_20171105_1845'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tempsubsection',
            options={'ordering': ['date_modified']},
        ),
        migrations.AlterField(
            model_name='tempnumerical',
            name='remarks',
            field=models.CharField(blank=True, help_text='For example: HSEB 2068, HSEB 2070 Frequently asked in Entrance, etc.', max_length=360),
        ),
        migrations.AlterField(
            model_name='tempsaq',
            name='remarks',
            field=models.CharField(blank=True, help_text='For example: HSEB 2068, HSEB 2070 Frequently asked in Entrance, etc.', max_length=360),
        ),
    ]