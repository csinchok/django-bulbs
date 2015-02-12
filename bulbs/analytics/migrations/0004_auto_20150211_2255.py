# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0003_auto_20150210_2112'),
    ]

    operations = [
        migrations.AddField(
            model_name='facebookpage',
            name='url',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='twitteraccount',
            name='allowed_hosts',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='twitteraccount',
            name='url',
            field=models.URLField(null=True, blank=True),
            preserve_default=True,
        ),
    ]
