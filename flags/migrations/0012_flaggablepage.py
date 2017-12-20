# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0032_add_bulk_delete_page_permission'),
        ('flags', '0011_migrate_path_data_startswith_to_matches'),
    ]

    operations = [
        migrations.CreateModel(
            name='FlaggablePage',
            fields=[
                ('page_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('feature_flag_name', models.CharField(max_length=64, blank=True)),
                ('show_draft_with_feature_flag', models.BooleanField(default=False, help_text=b"Whether a this page's latest draft will appear when the selected feature flag is enabled", verbose_name=b'show draft with feature flag')),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page', models.Model),
        ),
    ]
