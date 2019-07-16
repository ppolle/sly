# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-06-25 23:34
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shrink', '0007_slyurl_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slyurl',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='slyurls', to=settings.AUTH_USER_MODEL),
        ),
    ]