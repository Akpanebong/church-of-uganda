from django import forms
from .models import Invoice, Payment, Expense

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        exclude = ("created_at", "updated_at")
        widgets = {"issue_date": forms.DateInput(attrs={"type": "date"}), "due_date": forms.DateInput(attrs={"type": "date"})}

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        exclude = ("created_at", "updated_at")
        widgets = {"payment_date": forms.DateInput(attrs={"type": "date"})}

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        exclude = ("created_at", "updated_at")
        widgets = {"expense_date": forms.DateInput(attrs={"type": "date"})}
