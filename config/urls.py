from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.core.urls")),
    path("accounts/", include("apps.accounts.urls")),
    path("properties/", include("apps.properties.urls")),
    path("tenants/", include("apps.tenants.urls")),
    path("leases/", include("apps.leases.urls")),
    path("finance/", include("apps.finance.urls")),
    path("maintenance/", include("apps.maintenance.urls")),
    path("operations/", include("apps.operations.urls")),
    path("login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
