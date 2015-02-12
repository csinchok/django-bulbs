# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0004_auto_20150211_2255'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='facebookpost',
            name='content',
        ),
    ]
