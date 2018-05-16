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


class Positions(models.Model):
    position_id = models.CharField(primary_key=True, max_length=36)
    position_name = models.CharField(max_length=50)
    publish_date = models.DateField()
    education = models.CharField(max_length=3)
    work_year = models.CharField(max_length=5)
    job_nature = models.CharField(max_length=2)
    job_detail = models.CharField(max_length=5000)
    salary = models.CharField(max_length=20)
    city = models.CharField(max_length=10)
    district = models.CharField(max_length=20)
    job_address = models.CharField(max_length=100)
    company_name = models.CharField(max_length=30)
    second_type = models.CharField(max_length=5)
    first_type = models.CharField(max_length=10)
    url = models.CharField(max_length=100, unique=True)

    class Meta:
        managed = False
        db_table = 'positions'


class Urls(models.Model):
    url = models.ForeignKey(Positions, db_column='url', primary_key=True)
    intime = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'urls'


