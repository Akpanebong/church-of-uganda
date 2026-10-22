from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from .models import Invoice, Payment, Expense
from .forms import InvoiceForm, PaymentForm, ExpenseForm
from apps.core.crud import model_form_view, model_delete_view


@login_required
def finance_dashboard(request):
    return render(request,"finance/dashboard.html",{
        "invoices":Invoice.objects.order_by("-issue_date")[:10],
        "payments":Payment.objects.select_related("tenant").order_by("-payment_date")[:10],
        "total_billed":Invoice.objects.aggregate(v=Sum("amount"))["v"] or 0,
        "total_collected":Payment.objects.aggregate(v=Sum("amount"))["v"] or 0,
        "expenses":Expense.objects.aggregate(v=Sum("amount"))["v"] or 0,
    })


@login_required
def invoice_create(request):
    return model_form_view(request, Invoice, InvoiceForm,
                           "finance/invoice_form.html",
                           "finance_d", title="Invoice")


@login_required
def invoice_update(request, pk):
    return model_form_view(request, Invoice, InvoiceForm, "finance/invoice_form.html",
                           "finance_d", pk, "Invoice")


@login_required
def invoice_delete(request, pk):
    return model_delete_view(request, Invoice, "finance_d", pk,"Invoice")


@login_required
def payment_create(request):
    return model_form_view(request, Payment, PaymentForm, "finance/payment_form.html",
                           "finance_d", title="Payment")


@login_required
def payment_update(request, pk):
    return model_form_view(request, Payment, PaymentForm, "finance/payment_form.html",
                           "finance_d", pk, "Payment")


@login_required
def payment_delete(request, pk):
    return model_delete_view(request, Payment, "finance_d", pk, "Payment")


@login_required
def expense_create(request):
    return model_form_view(request, Expense, ExpenseForm, "finance/expense_form.html",
                           "finance_d", title="Expense")


@login_required
def expense_update(request, pk):
    return model_form_view(request, Expense, ExpenseForm, "finance/expense_form.html",
                           "finance_d", pk, "Expense")


@login_required
def expense_delete(request, pk):
    return model_delete_view(request, Expense, "finance_d", pk, "Expense")
