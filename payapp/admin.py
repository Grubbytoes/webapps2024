from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from payapp import models

# Register your models here.
admin.site.register(models.UserAccount, UserAdmin)