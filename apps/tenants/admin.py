from django.contrib import admin
from .models import Tenant, TenantUnit
admin.site.register([Tenant, TenantUnit])
