# /accounts/admin.py (or your app's admin.py)

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

# Register the User model with the built-in UserAdmin
admin.site.register(User, UserAdmin)