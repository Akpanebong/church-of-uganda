from django.urls import path
from .views import (dashboard, notifications, diocese_profile, diocese_profile_list,
                    diocese_profile_detail, diocese_profile_create, diocese_profile_update,
                    diocese_profile_trash, diocese_profile_delete, estate_document_list,
                    estate_document_create, estate_document_update, estate_document_delete,
                    global_search)
urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("notifications/", notifications, name="notifications"),
    path("search/", global_search, name="global_search"),
    path("diocese-profile/", diocese_profile, name="diocese_profile"),
    path("diocese-profile/list/", diocese_profile_list, name="diocese_profile_list"),
    path("diocese-profile/new/", diocese_profile_create, name="diocese_profile_create"),
    path("diocese-profile/<int:pk>/", diocese_profile_detail, name="diocese_profile_detail"),
    path("diocese-profile/<int:pk>/edit/", diocese_profile_update, name="diocese_profile_update"),
    path("diocese-profile/<int:pk>/trash/", diocese_profile_trash, name="diocese_profile_trash"),
    path("diocese-profile/<int:pk>/delete/", diocese_profile_delete, name="diocese_profile_delete"),
    path("records/", estate_document_list, name="estate_document_list"),
    path("records/new/", estate_document_create, name="estate_document_create"),
    path("records/<int:pk>/edit/", estate_document_update, name="estate_document_update"),
    path("records/<int:pk>/delete/", estate_document_delete, name="estate_document_delete"),
]
