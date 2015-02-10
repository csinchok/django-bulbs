# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_add_groups'),
    ]

    operations = [
        migrations.CreateModel(
            name='FacebookPage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_checked', models.DateTimeField(null=True, blank=True)),
                ('name', models.CharField(max_length=255)),
                ('page_id', models.IntegerField()),
                ('access_token', models.CharField(max_length=510)),
                ('allowed_hosts', models.CharField(max_length=255, null=True, blank=True)),
                ('last_updated', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FacebookPost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('post_id', models.CharField(max_length=255)),
                ('data', models.TextField(null=True, blank=True)),
                ('insights', models.TextField(null=True, blank=True)),
                ('last_updated', models.DateTimeField()),
                ('content', models.ForeignKey(blank=True, to='content.Content', null=True)),
                ('page', models.ForeignKey(related_name='posts', to='analytics.FacebookPage')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TwitterAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_checked', models.DateTimeField(null=True, blank=True)),
                ('handle', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
