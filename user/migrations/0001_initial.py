# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, db_column='Id', serialize=False)),
                ('user_name', models.CharField(max_length=13)),
                ('user_pwd', models.CharField(max_length=40)),
                ('user_email', models.CharField(max_length=25)),
                ('user_code', models.CharField(null=True, blank=True, max_length=100)),
                ('user_key', models.CharField(null=True, blank=True, max_length=40)),
                ('user_rank', models.IntegerField(default=0)),
            ],
            options={
                'managed': False,
                'db_table': 'user',
            },
        ),
    ]
