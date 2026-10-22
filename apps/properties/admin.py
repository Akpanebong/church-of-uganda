from django.contrib import admin
from .models import Property, Building, Unit
admin.site.register([Property, Building, Unit])
