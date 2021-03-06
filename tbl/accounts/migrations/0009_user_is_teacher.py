# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-21 01:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_remove_user_is_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_teacher',
            field=models.BooleanField(default=False, help_text='Verify if the user is teacher or student', verbose_name='Is Teacher?'),
        ),
    ]
