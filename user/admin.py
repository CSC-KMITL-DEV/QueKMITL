from django.contrib import admin
from django.contrib.auth.models import Permission
from user.models import User_in_type
from provider.models import TypeUser

# Register your models here.
class User_in_typeAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_type', 'user']


admin.site.register(Permission)
admin.site.register(User_in_type, User_in_typeAdmin)