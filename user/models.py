# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class User(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    user_name = models.CharField(max_length=13, unique=True)
    user_pwd = models.CharField(max_length=40)
    user_email = models.CharField(max_length=25, unique=True)
    user_code = models.CharField(max_length=100, blank=True, null=True, unique=True)
    user_key = models.CharField(max_length=40, blank=True, null=True, unique=True)
    user_rank = models.IntegerField(default=0)

    # user_code:激活码，当激活成功后为None
    # user_key:创建用户的时候自动生成，用于请求api是的key

    class Meta:
        managed = False
        db_table = 'user'
