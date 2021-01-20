from django.contrib import admin
from .models import gameIdentifier,gamePost 
from reports.models import Report
admin.site.register(gameIdentifier)
admin.site.register(gamePost)
admin.site.register(Report)