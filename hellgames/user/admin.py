from django.contrib import admin
from user.models import Profile, CustomUser, Reviews

admin.site.register(Profile)
admin.site.register(CustomUser)
admin.site.register(Reviews)