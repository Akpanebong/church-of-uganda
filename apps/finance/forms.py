from django import forms
from .models import Invoice, Payment, Expense


class InvoiceForm(forms.ModelForm):
    def clean(self):
        cleaned = super().clean()
        lease = cleaned.get("lease")
        if lease:
            cleaned["due_date"] = lease.end_date
        return cleaned

    class Meta:
        model = Invoice
        exclude = ("created_at", "updated_at")
        widgets = {"issue_date": forms.DateInput(attrs={"type": "date"}),
                   "due_date": forms.DateInput(attrs={"type": "date"}),
                   }


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        exclude = ("created_at", "updated_at", "receipt_number", "reference")
        widgets = {"payment_date": forms.DateInput(attrs={"type": "date"}),
                   'notes': forms.Textarea(attrs={"rows": 2, "cols": 15, 'class': 'form-control'}),
                   }

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        exclude = ("created_at", "updated_at")
        widgets = {"expense_date": forms.DateInput(attrs={"type": "date"})}
