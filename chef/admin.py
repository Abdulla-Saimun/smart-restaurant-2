from django.contrib import admin
from .models import chef_account


# Register your models here.
class ChefAdmin(admin.ModelAdmin):
    list_display = ('chef_userid', 'chef_fullname', 'chef_email', 'chef_phone')


admin.site.register(chef_account, ChefAdmin)
