# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-28 13:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='numerical',
            name='subtopic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cms.Subtopic'),
        ),
        migrations.AlterField(
            model_name='saq',
            name='subtopic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cms.Subtopic'),
        ),
    ]
