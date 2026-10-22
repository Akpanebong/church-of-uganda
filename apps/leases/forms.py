
from django import forms
from django.db.models import Q

from apps.leases.models import Lease
from apps.properties.models import Unit
from apps.tenants.models import Tenant


class LeaseForm(forms.ModelForm):
    unit = forms.ModelChoiceField(
        queryset=Unit.objects.none(),
        empty_label="Select available unit",
        help_text="Only available units and the unit already assigned to this lease.",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    tenant = forms.ModelChoiceField(
        queryset=Tenant.objects.filter(status="active").order_by("full_name"),
        empty_label="Select active tenant",
        help_text="Only tenants with Active status.",
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Lease
        exclude = ("created_at", "updated_at")
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
            "terms": forms.Textarea(attrs={"rows": 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # New leases can select only available units.
        units = Unit.objects.filter(status="available")

        # Existing leases can also retain their currently assigned unit.
        if self.instance and self.instance.pk and self.instance.unit_id:
            units = Unit.objects.filter(
                Q(status="available")
                | Q(pk=self.instance.unit_id)
            )

            current_unit = self.instance.unit
            self.fields["rent"].widget.attrs["data-default-value"] = str(
                current_unit.monthly_rent
            )
            self.fields["service_charge"].widget.attrs["data-default-value"] = str(
                current_unit.service_charge
            )

        self.fields["unit"].queryset = (
            units.select_related("property", "building")
            .order_by("-monthly_rent", "unit_number")
        )

    def clean(self):
        cleaned = super().clean()
        unit = cleaned.get("unit")

        if unit:
            if cleaned.get("rent") in (None, ""):
                cleaned["rent"] = unit.monthly_rent

            if cleaned.get("service_charge") in (None, ""):
                cleaned["service_charge"] = unit.service_charge

        return cleaned
