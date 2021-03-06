# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-11 19:58
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('network', '0003_auto_20170304_1937'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Firstname', models.CharField(max_length=20)),
                ('Lastname', models.CharField(max_length=20)),
                ('Age', models.CharField(blank=True, max_length=3, null=True)),
                ('Short_bio', models.CharField(blank=True, max_length=430)),
                ('photo', models.FileField(blank=True, default='empty.jpg', upload_to='images')),
                ('content_type', models.CharField(max_length=50)),
                ('Follows', models.ManyToManyField(related_name='follow_list', to='network.Profile')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
