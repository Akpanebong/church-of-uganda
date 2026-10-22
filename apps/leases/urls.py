from django.urls import path
from .views import lease_list, lease_create, lease_update, lease_delete, unit_details
urlpatterns=[path("",lease_list,name="lease_list"), path("new/",lease_create,name="lease_create"), path("units/<int:pk>/details/",unit_details,name="unit_details"), path("<int:pk>/edit/",lease_update,name="lease_update"), path("<int:pk>/delete/",lease_delete,name="lease_delete")]
