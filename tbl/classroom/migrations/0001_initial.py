# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-29 17:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('discipline', '0001_initial'),
        ('accounts', '0009_user_is_teacher'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassRoom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Title of class', max_length=100, verbose_name='Title')),
                ('password', models.CharField(help_text='Class access password', max_length=20, verbose_name='Password')),
                ('student_limit', models.PositiveIntegerField(help_text='Maximum number of students in the class', verbose_name='Student Limit')),
                ('is_closed', models.BooleanField(default=False, verbose_name='Is closed?')),
                ('discipline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classes', related_query_name='class', to='discipline.Discipline')),
                ('students', models.ManyToManyField(to='accounts.Student')),
            ],
            options={
                'verbose_name_plural': 'Classes',
                'ordering': ('title',),
                'verbose_name': 'ClassRoom',
            },
        ),
    ]