
from django import forms
from django.db.models import Q

from apps.leases.models import Lease
from apps.properties.models import Unit
from apps.tenants.models import Tenant
from apps.finance.models import Payment


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
        exclude = ("created_at", "updated_at", "lease_number", 'expiry_notice_sent')
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
            "terms": forms.Textarea(attrs={"rows": 1, 'class': 'form-control'}),
        }

    def __init__(self, *args, include_initial_payment=False, **kwargs):
        super().__init__(*args, **kwargs)

        if include_initial_payment:
            self.fields["deposit"].help_text = (
                "This deposit will be recorded as the initial payment against the lease invoice."
            )
            self.fields["initial_payment_date"] = forms.DateField(
                required=False,
                label="Initial payment date",
                widget=forms.DateInput(attrs={"type": "date"}),
            )
            self.fields["initial_payment_method"] = forms.ChoiceField(
                required=False,
                label="Payment method",
                choices=[("", "Select payment method")] + list(Payment.METHODS),
            )

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

        if "initial_payment_date" in self.fields:
            payment_amount = cleaned.get("deposit") or 0
            payment_date = cleaned.get("initial_payment_date")
            payment_method = cleaned.get("initial_payment_method")
            if payment_amount and not payment_date:
                self.add_error("initial_payment_date", "Enter the payment date.")
            if payment_amount and not payment_method:
                self.add_error("initial_payment_method", "Select the payment method.")
            if (payment_date or payment_method) and not payment_amount:
                self.add_error("deposit", "Enter a deposit amount before recording a payment.")

        return cleaned
