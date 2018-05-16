# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Positions',
            fields=[
                ('position_id', models.CharField(serialize=False, primary_key=True, max_length=36)),
                ('position_name', models.CharField(max_length=50)),
                ('publish_date', models.DateField()),
                ('education', models.CharField(max_length=3)),
                ('work_year', models.CharField(max_length=5)),
                ('job_nature', models.CharField(max_length=2)),
                ('job_detail', models.CharField(max_length=5000)),
                ('salary', models.CharField(max_length=20)),
                ('city', models.CharField(max_length=10)),
                ('district', models.CharField(max_length=20)),
                ('job_address', models.CharField(max_length=100)),
                ('company_name', models.CharField(max_length=30)),
                ('second_type', models.CharField(max_length=5)),
                ('first_type', models.CharField(max_length=10)),
                ('url', models.CharField(max_length=100)),
            ],
            options={
                'managed': False,
                'db_table': 'positions',
            },
        ),
        migrations.CreateModel(
            name='Urls',
            fields=[
                ('url', models.ForeignKey(db_column='url', to='search.Positions', serialize=False, primary_key=True)),
                ('intime', models.DateTimeField()),
            ],
            options={
                'managed': False,
                'db_table': 'urls',
            },
        ),
    ]
