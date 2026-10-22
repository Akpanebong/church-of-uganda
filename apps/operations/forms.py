from django import forms

from .models import (
    Inspection,
    UtilityMeter,
    MeterReading,
    Asset,
    Contractor,
    Visitor,
    ParkingSpace,
    ComplianceItem,
    DevelopmentProject,
    LandDispute,
    RiskRegisterItem,
)


# ---------------------------------------------------------------------
# Shared widget configuration
# ---------------------------------------------------------------------

class EstatesModelForm(forms.ModelForm):
    """Shared Bootstrap styling for Estates Management model forms."""

    DATE_FIELDS = ()
    DATETIME_FIELDS = ()
    TEXT_FIELDS = ()
    NUMBER_FIELDS = ()
    CHECKBOX_FIELDS = ()
    SELECT_FIELDS = ()

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            widget = field.widget
            existing = widget.attrs.copy()

            # Keep existing widget attributes and CSS classes.
            if isinstance(widget, forms.CheckboxInput):
                existing["class"] = (
                    f"{existing.get('class', '')} form-check-input".strip()
                )
            elif isinstance(widget, forms.HiddenInput):
                pass
            else:
                existing["class"] = (
                    f"{existing.get('class', '')} form-select"
                    if isinstance(widget, (forms.Select, forms.SelectMultiple))
                    else f"{existing.get('class', '')} form-control"
                ).strip()

            # Compact textareas for descriptions, notes and recommendations.
            if isinstance(widget, forms.Textarea):
                existing.setdefault("rows", 2)
                existing.setdefault("class", "form-control")
                existing.setdefault("placeholder", f"Enter {field.label.lower()}")

            # Date and date-time fields.
            if name in self.DATE_FIELDS:
                widget.input_type = "date"

            if name in self.DATETIME_FIELDS:
                widget.input_type = "datetime-local"

            # Numeric fields.
            if isinstance(widget, forms.NumberInput):
                existing.setdefault("step", "any")

            # Consistent accessibility and browser validation.
            existing.setdefault("id", f"id_{name}")

            if field.required:
                existing.setdefault("aria-required", "true")

            widget.attrs = existing

            # Useful labels and help text can be customized per form.
            if name in self.TEXT_FIELDS and isinstance(widget, forms.Textarea):
                widget.attrs.setdefault("maxlength", field.max_length or "")

            # Preserve Django's normal validation and model field requirements.


# ---------------------------------------------------------------------
# Inspections
# ---------------------------------------------------------------------

class InspectionForm(EstatesModelForm):
    DATE_FIELDS = ("inspection_date",)
    TEXT_FIELDS = ("recommendations",)

    class Meta:
        model = Inspection
        exclude = ("created_at", "updated_at")
        widgets = {
            "inspection_date": forms.DateInput(attrs={"type": "date"}),
            "inspector": forms.TextInput(attrs={
                "placeholder": "Inspector's full name",
            }),
            "condition": forms.TextInput(attrs={
                "placeholder": "e.g. Good, Fair, Requires repair",
            }),
            "recommendations": forms.Textarea(attrs={
                "rows": 2,
                "placeholder": "Record findings and recommended actions",
            }),
        }


# ---------------------------------------------------------------------
# Utility meters and readings
# ---------------------------------------------------------------------

class UtilityMeterForm(EstatesModelForm):
    class Meta:
        model = UtilityMeter
        exclude = ("created_at", "updated_at")
        widgets = {
            "meter_number": forms.TextInput(attrs={
                "placeholder": "Enter the meter reference number",
            }),
        }


class MeterReadingForm(EstatesModelForm):
    DATE_FIELDS = ("reading_date",)
    TEXT_FIELDS = ("notes",)

    class Meta:
        model = MeterReading
        exclude = ("created_at", "updated_at")
        widgets = {
            "reading_date": forms.DateInput(attrs={"type": "date"}),
            "reading": forms.NumberInput(attrs={
                "min": "0",
                "step": "any",
                "placeholder": "Current meter reading",
            }),
            "previous_reading": forms.NumberInput(attrs={
                "min": "0",
                "step": "any",
                "placeholder": "Previous meter reading",
            }),
            "notes": forms.Textarea(attrs={
                "rows": 2,
                "placeholder": "Optional reading notes",
            }),
        }


# ---------------------------------------------------------------------
# Estate assets
# ---------------------------------------------------------------------

class AssetForm(EstatesModelForm):
    DATE_FIELDS = ("purchase_date", "warranty_expiry")
    TEXT_FIELDS = ("notes",)

    class Meta:
        model = Asset
        exclude = ("created_at", "updated_at")
        widgets = {
            "asset_code": forms.TextInput(attrs={
                "placeholder": "Unique asset identification code",
            }),
            "name": forms.TextInput(attrs={
                "placeholder": "Asset name",
            }),
            "purchase_date": forms.DateInput(attrs={"type": "date"}),
            "warranty_expiry": forms.DateInput(attrs={"type": "date"}),
            "purchase_cost": forms.NumberInput(attrs={
                "min": "0",
                "step": "0.01",
                "placeholder": "Purchase cost",
            }),
            "notes": forms.Textarea(attrs={
                "rows": 2,
                "placeholder": "Condition details, serial number or other notes",
            }),
        }


# ---------------------------------------------------------------------
# Contractors
# ---------------------------------------------------------------------

class ContractorForm(EstatesModelForm):
    TEXT_FIELDS = ("address",)

    class Meta:
        model = Contractor
        exclude = ("created_at", "updated_at")
        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Contractor or company name",
            }),
            "service": forms.TextInput(attrs={
                "placeholder": "e.g. Plumbing, electrical, construction",
            }),
            "phone": forms.TextInput(attrs={
                "type": "tel",
                "placeholder": "Contact telephone number",
            }),
            "email": forms.EmailInput(attrs={
                "placeholder": "name@example.com",
            }),
            "address": forms.Textarea(attrs={
                "rows": 2,
                "placeholder": "Contractor's business address",
            }),
        }


# ---------------------------------------------------------------------
# Visitors
# ---------------------------------------------------------------------

class VisitorForm(EstatesModelForm):
    DATETIME_FIELDS = ("check_in", "check_out")

    class Meta:
        model = Visitor
        exclude = ("created_at", "updated_at")
        widgets = {
            "host_name": forms.TextInput(attrs={
                "placeholder": "Person or office being visited",
            }),
            "visitor_name": forms.TextInput(attrs={
                "placeholder": "Visitor's full name",
            }),
            "phone": forms.TextInput(attrs={
                "type": "tel",
                "placeholder": "Visitor's contact number",
            }),
            "vehicle_registration": forms.TextInput(attrs={
                "placeholder": "Vehicle registration, if applicable",
            }),
            "purpose": forms.Textarea(attrs={
                "rows": 2,
                "placeholder": "Purpose of visit",
            }),
            "check_in": forms.DateTimeInput(attrs={
                "type": "datetime-local",
            }),
            "check_out": forms.DateTimeInput(attrs={
                "type": "datetime-local",
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get("check_in")
        check_out = cleaned_data.get("check_out")

        if check_in and check_out and check_out < check_in:
            self.add_error(
                "check_out",
                "Check-out time cannot be earlier than check-in time.",
            )

        return cleaned_data


# ---------------------------------------------------------------------
# Parking
# ---------------------------------------------------------------------

class ParkingSpaceForm(EstatesModelForm):
    class Meta:
        model = ParkingSpace
        exclude = ("created_at", "updated_at")
        widgets = {
            "space_number": forms.TextInput(attrs={
                "placeholder": "Parking space number",
            }),
            "assigned_to": forms.TextInput(attrs={
                "placeholder": "Assigned person or organisation",
            }),
            "vehicle_registration": forms.TextInput(attrs={
                "placeholder": "Vehicle registration number",
            }),
            "monthly_fee": forms.NumberInput(attrs={
                "min": "0",
                "step": "0.01",
                "placeholder": "Monthly parking fee",
            }),
        }


# ---------------------------------------------------------------------
# Compliance and statutory obligations
# ---------------------------------------------------------------------

class ComplianceItemForm(EstatesModelForm):
    DATE_FIELDS = ("expiry_date",)
    TEXT_FIELDS = ("notes",)

    class Meta:
        model = ComplianceItem
        exclude = ("created_at", "updated_at")
        widgets = {
            "title": forms.TextInput(attrs={
                "placeholder": "Permit, licence or compliance requirement",
            }),
            "reference": forms.TextInput(attrs={
                "placeholder": "Document or compliance reference",
            }),
            "expiry_date": forms.DateInput(attrs={"type": "date"}),
            "status": forms.TextInput(attrs={
                "placeholder": "e.g. Valid, Pending, Expired",
            }),
            "notes": forms.Textarea(attrs={
                "rows": 2,
                "placeholder": "Compliance notes or required follow-up",
            }),
        }


# ---------------------------------------------------------------------
# Development projects
# ---------------------------------------------------------------------

class DevelopmentProjectForm(EstatesModelForm):
    DATE_FIELDS = ("start_date", "target_date")
    TEXT_FIELDS = ("description",)

    class Meta:
        model = DevelopmentProject
        exclude = ("created_at", "updated_at")
        widgets = {
            "project_code": forms.TextInput(attrs={
                "placeholder": "Unique project code",
            }),
            "name": forms.TextInput(attrs={
                "placeholder": "Development project name",
            }),
            "sponsor": forms.TextInput(attrs={
                "placeholder": "Funding organisation or sponsor",
            }),
            "description": forms.Textarea(attrs={
                "rows": 2,
                "placeholder": "Scope, objectives and expected outcomes",
            }),
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "target_date": forms.DateInput(attrs={"type": "date"}),
            "approved_budget": forms.NumberInput(attrs={
                "min": "0",
                "step": "0.01",
                "placeholder": "Approved project budget",
            }),
            "spent_amount": forms.NumberInput(attrs={
                "min": "0",
                "step": "0.01",
                "placeholder": "Amount spent to date",
            }),
            "approval_reference": forms.TextInput(attrs={
                "placeholder": "Approval minute or reference number",
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        target_date = cleaned_data.get("target_date")
        budget = cleaned_data.get("approved_budget")
        spent = cleaned_data.get("spent_amount")

        if start_date and target_date and target_date < start_date:
            self.add_error(
                "target_date",
                "The target date cannot be earlier than the start date.",
            )

        if budget is not None and spent is not None and spent < 0:
            self.add_error("spent_amount", "Amount spent cannot be negative.")

        return cleaned_data


# ---------------------------------------------------------------------
# Land disputes
# ---------------------------------------------------------------------

class LandDisputeForm(EstatesModelForm):
    DATE_FIELDS = ("next_action_date",)
    TEXT_FIELDS = ("summary", "resolution")

    class Meta:
        model = LandDispute
        exclude = ("created_at", "updated_at")
        widgets = {
            "reference": forms.TextInput(attrs={
                "placeholder": "Unique dispute reference",
            }),
            "claimant": forms.TextInput(attrs={
                "placeholder": "Claimant's name or organisation",
            }),
            "summary": forms.Textarea(attrs={
                "rows": 2,
                "placeholder": "Nature of claim, location and key facts",
            }),
            "assigned_officer": forms.TextInput(attrs={
                "placeholder": "Responsible officer",
            }),
            "next_action_date": forms.DateInput(attrs={"type": "date"}),
            "resolution": forms.Textarea(attrs={
                "rows": 2,
                "placeholder": "Resolution details, if resolved",
            }),
        }


# ---------------------------------------------------------------------
# Risk register
# ---------------------------------------------------------------------

class RiskRegisterItemForm(EstatesModelForm):
    DATE_FIELDS = ("review_date",)
    TEXT_FIELDS = ("description", "mitigation")

    class Meta:
        model = RiskRegisterItem
        exclude = ("created_at", "updated_at")
        widgets = {
            "reference": forms.TextInput(attrs={
                "placeholder": "Unique risk reference",
            }),
            "risk_title": forms.TextInput(attrs={
                "placeholder": "Short, specific risk title",
            }),
            "description": forms.Textarea(attrs={
                "rows": 2,
                "placeholder": "Describe the risk, cause and potential consequence",
            }),
            "mitigation": forms.Textarea(attrs={
                "rows": 2,
                "placeholder": "Controls, mitigation measures and contingency actions",
            }),
            "owner": forms.TextInput(attrs={
                "placeholder": "Risk owner or responsible officer",
            }),
            "review_date": forms.DateInput(attrs={"type": "date"}),
            "status": forms.TextInput(attrs={
                "placeholder": "e.g. Open, In Progress, Closed",
            }),
        }