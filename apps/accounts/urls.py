from django.contrib.auth import views as auth_views
from django.urls import path
from .views import staff_register, staff_profile, StaffPasswordChangeView, StaffPasswordResetView, StaffPasswordResetDoneView, StaffPasswordResetConfirmView, StaffPasswordResetCompleteView

urlpatterns = [
    path("register/", staff_register, name="staff_register"), path("profile/", staff_profile, name="staff_profile"),
    path("password/change/", StaffPasswordChangeView.as_view(), name="password_change"),
    path("password/reset/", StaffPasswordResetView.as_view(), name="password_reset"),
    path("password/reset/done/", StaffPasswordResetDoneView.as_view(), name="password_reset_done"),
    path("password/reset/<uidb64>/<token>/", StaffPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("password/reset/complete/", StaffPasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
