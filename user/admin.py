from django.contrib import admin
from user import models

class UserAdmin(admin.ModelAdmin):
    list_display = ['pk','user_name']

admin.site.register(models.User,UserAdmin)

