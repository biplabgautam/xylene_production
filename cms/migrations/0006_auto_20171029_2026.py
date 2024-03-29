# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-29 14:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0005_auto_20171025_2000'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chapter',
            options={'ordering': ['chapter_serial'], 'permissions': (('create_chapter', 'Can create new chapters.'), ('edit_chapter', 'Can edit existing chapter.'))},
        ),
        migrations.AlterModelOptions(
            name='numerical',
            options={'ordering': ['numerical_serial'], 'permissions': (('create_numerical', 'Can create new numericals.'), ('edit_numerical', 'Can edit existing numerical.'))},
        ),
        migrations.AlterModelOptions(
            name='saq',
            options={'ordering': ['question_serial'], 'permissions': (('create_SAQ', 'Can create new SAQs.'), ('edit_SAQ', 'Can edit existing SAQ.'))},
        ),
        migrations.AlterModelOptions(
            name='subject',
            options={'permissions': (('create_subject', 'Can create new subjects.'), ('edit_subject', 'Can edit existing subject.'))},
        ),
        migrations.AlterModelOptions(
            name='subsection',
            options={'ordering': ['subsection_serial'], 'permissions': (('create_subsection', 'Can create new subsections.'), ('edit_subsection', 'Can edit existing subsection.'))},
        ),
        migrations.AlterModelOptions(
            name='subsectionimage',
            options={'permissions': (('create_subsectionImage', 'Can create new Subsection Images.'), ('edit_subsectionImage', 'Can edit existing Subsection Images.'))},
        ),
        migrations.AlterModelOptions(
            name='subtopic',
            options={'ordering': ['subtopic_serial'], 'permissions': (('create_subtopic', 'Can create new subtopics.'), ('edit_subtopic', 'Can edit existing subtopic.'))},
        ),
    ]
