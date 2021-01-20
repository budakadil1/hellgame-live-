from django.urls import path, include
from . import views

app_name = 'reports'
urlpatterns = [
    path('', views.index, name='index'),
    path('checkstatus/<uuid:report_id>', views.checkstatus, name="status")
]
