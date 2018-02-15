# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-29 15:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0006_auto_20171029_2026'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chapter',
            options={'ordering': ['chapter_serial']},
        ),
        migrations.AlterModelOptions(
            name='numerical',
            options={'ordering': ['numerical_serial']},
        ),
        migrations.AlterModelOptions(
            name='saq',
            options={'ordering': ['question_serial']},
        ),
        migrations.AlterModelOptions(
            name='subject',
            options={},
        ),
        migrations.AlterModelOptions(
            name='subsection',
            options={'ordering': ['subsection_serial']},
        ),
        migrations.AlterModelOptions(
            name='subsectionimage',
            options={},
        ),
        migrations.AlterModelOptions(
            name='subtopic',
            options={'ordering': ['subtopic_serial']},
        ),
    ]
