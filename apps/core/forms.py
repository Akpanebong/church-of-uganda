from django import forms
from .models import DioceseProfile, EstateDocument

class DioceseProfileForm(forms.ModelForm):
    class Meta:
        model = DioceseProfile
        exclude = ("created_at", "updated_at")
        widgets = {"effective_date": forms.DateInput(attrs={"type": "date"}), "review_date": forms.DateInput(attrs={"type": "date"}), "approval_date": forms.DateInput(attrs={"type": "date"})}

class EstateDocumentForm(forms.ModelForm):
    class Meta:
        model = EstateDocument
        exclude = ("created_at", "updated_at", "owner")
        widgets = {"effective_date": forms.DateInput(attrs={"type": "date"}),
                   "description": forms.Textarea(attrs={"rows": 5, "cols": 2}),}
