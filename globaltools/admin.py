from django.contrib import admin
from . import models as mymodels


@admin.register(mymodels.UserAccount)
class UserAccountAdmin(admin.ModelAdmin):
    pass
