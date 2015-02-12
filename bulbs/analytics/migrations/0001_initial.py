# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_add_groups'),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_checked', models.DateTimeField(null=True, blank=True)),
                ('url', models.URLField(null=True, blank=True)),
                ('allowed_hosts', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FacebookPage',
            fields=[
                ('socialaccount_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='analytics.SocialAccount')),
                ('name', models.CharField(max_length=255)),
                ('page_id', models.BigIntegerField()),
                ('access_token', models.CharField(max_length=510)),
            ],
            options={
                'abstract': False,
            },
            bases=('analytics.socialaccount',),
        ),
        migrations.CreateModel(
            name='SocialPromotion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(null=True, blank=True)),
                ('created_time', models.DateTimeField()),
                ('last_updated', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'ordering': ('-created_time',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FacebookPost',
            fields=[
                ('socialpromotion_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='analytics.SocialPromotion')),
                ('post_id', models.CharField(max_length=255)),
                ('data', models.TextField(null=True, blank=True)),
                ('insights', models.TextField(null=True, blank=True)),
                ('page', models.ForeignKey(related_name='posts', to='analytics.FacebookPage')),
            ],
            options={
                'abstract': False,
            },
            bases=('analytics.socialpromotion',),
        ),
        migrations.CreateModel(
            name='TwitterAccount',
            fields=[
                ('socialaccount_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='analytics.SocialAccount')),
                ('handle', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
            bases=('analytics.socialaccount',),
        ),
        migrations.AddField(
            model_name='socialpromotion',
            name='content',
            field=models.ForeignKey(blank=True, to='content.Content', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='socialpromotion',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_analytics.socialpromotion_set', editable=False, to='contenttypes.ContentType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='socialaccount',
            name='polymorphic_ctype',
            field=models.ForeignKey(related_name='polymorphic_analytics.socialaccount_set', editable=False, to='contenttypes.ContentType', null=True),
            preserve_default=True,
        ),
    ]
