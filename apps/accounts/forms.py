from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

User = get_user_model()

class StaffRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True
        if commit: user.save()
        return user

class StaffProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username")
