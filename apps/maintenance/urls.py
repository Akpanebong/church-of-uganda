from django.urls import path
from .views import maintenance_list, maintenance_create, maintenance_update, maintenance_delete
urlpatterns=[path("",maintenance_list,name="maintenance_list"), path("new/",maintenance_create,name="maintenance_create"), path("<int:pk>/edit/",maintenance_update,name="maintenance_update"), path("<int:pk>/delete/",maintenance_delete,name="maintenance_delete")]
