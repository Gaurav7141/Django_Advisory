from django.contrib import admin

from .models import Result,EmailCredentials
# Unregister User model from auth.UserAdmin
# admin.site.unregister(User)

# Register User model with your custom UserAdmin or the default UserAdmin
admin.site.register(Result)
admin.site.register(EmailCredentials)

