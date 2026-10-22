from django.contrib import admin
from .models import Notification, AuditLog, DioceseProfile, EstateDocument
admin.site.register([Notification, AuditLog, DioceseProfile, EstateDocument])
