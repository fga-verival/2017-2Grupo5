# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-30 05:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20170730_0351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='tags',
            field=models.ManyToManyField(related_name='tags', related_query_name='news', to='core.Tag'),
        ),
    ]