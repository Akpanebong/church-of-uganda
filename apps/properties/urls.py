from django.urls import path
from .views import (property_list, property_detail, property_create, property_update, property_delete,
                    building_create, building_update, building_delete, unit_create, unit_update, unit_delete)
urlpatterns=[
    path("", property_list, name="property_list"), path("new/", property_create, name="property_create"),
    path("<int:pk>/", property_detail, name="property_detail"), path("<int:pk>/edit/", property_update, name="property_update"), path("<int:pk>/delete/", property_delete, name="property_delete"),
    path("buildings/new/", building_create, name="building_create"), path("buildings/<int:pk>/edit/", building_update, name="building_update"), path("buildings/<int:pk>/delete/", building_delete, name="building_delete"),
    path("units/new/", unit_create, name="unit_create"), path("units/<int:pk>/edit/", unit_update, name="unit_update"), path("units/<int:pk>/delete/", unit_delete, name="unit_delete"),
]
