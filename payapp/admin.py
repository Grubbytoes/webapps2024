from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin
from payapp import models

# Register your models here.
admin.site.register(models.UserAccount, UserAdmin)
admin.site.register(models.Holding, ModelAdmin)
admin.site.register(models.Transaction, ModelAdmin)
admin.site.register(models.Request, ModelAdmin)
admin.site.register(models.Notification, ModelAdmin)