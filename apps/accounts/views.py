from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from .forms import StaffRegistrationForm, StaffProfileForm

def staff_register(request):
    form = StaffRegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save(); login(request, user); messages.success(request, "Your staff account has been created."); return redirect("dashboard")
    return render(request, "accounts/register.html", {"form": form})

@login_required
def staff_profile(request):
    form = StaffProfileForm(request.POST or None, instance=request.user)
    if request.method == "POST" and form.is_valid(): form.save(); messages.success(request, "Your profile was updated."); return redirect("staff_profile")
    return render(request, "accounts/profile.html", {"form": form})

class StaffPasswordChangeView(PasswordChangeView):
    template_name = "accounts/password_change.html"
    success_url = reverse_lazy("staff_profile")
    def form_valid(self, form):
        messages.success(self.request, "Your password was changed successfully.")
        return super().form_valid(form)

class StaffPasswordResetView(PasswordResetView):
    template_name = "accounts/password_reset.html"
    email_template_name = "accounts/password_reset_email.txt"
    subject_template_name = "accounts/password_reset_subject.txt"
    success_url = reverse_lazy("password_reset_done")

class StaffPasswordResetDoneView(PasswordResetDoneView):
    template_name = "accounts/password_reset_done.html"
class StaffPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "accounts/password_reset_confirm.html"
    success_url = reverse_lazy("password_reset_complete")
class StaffPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "accounts/password_reset_complete.html"
