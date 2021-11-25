from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'username',)

admin.site.register(User, UserAdmin)