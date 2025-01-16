from django.contrib import admin
from .models import User, Profile


# Registering the models to the admin site
admin.site.register(User)
admin.site.register(Profile)
