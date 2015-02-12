# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_add_groups'),
        ('contenttypes', '0001_initial'),
        ('analytics', '0005_remove_facebookpost_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialPromotion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(null=True, blank=True)),
                ('created_time', models.DateTimeField()),
                ('last_updated', models.DateTimeField(null=True, blank=True)),
                ('content', models.ForeignKey(blank=True, to='content.Content', null=True)),
                ('polymorphic_ctype', models.ForeignKey(related_name='polymorphic_analytics.socialpromotion_set', editable=False, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'ordering': ('-created_time',),
            },
            bases=(models.Model,),
        ),
    ]
