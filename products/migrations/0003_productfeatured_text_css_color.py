# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20170805_1757'),
    ]

    operations = [
        migrations.AddField(
            model_name='productfeatured',
            name='text_css_color',
            field=models.CharField(max_length=6, null=True, blank=True),
        ),
    ]