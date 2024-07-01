from django.contrib import admin
from .models import URL, User
from django.contrib.auth.admin import UserAdmin


# Register your models here.
class UserAdmin(admin.ModelAdmin):  
    list_display = ('id','first_name', 'last_name', 'email')

admin.site.register(User, UserAdmin)
admin.site.register(URL)
