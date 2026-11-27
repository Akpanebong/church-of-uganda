from django.contrib.auth.decorators import login_required
from decimal import Decimal
from datetime import date
from django.db.models import Case, DecimalField, ExpressionWrapper, F, Q, Sum, Value, When
from django.db.models.functions import Coalesce
from django.shortcuts import render
from django.utils import timezone
from .models import Invoice, Payment, Expense
from .forms import InvoiceForm, PaymentForm, ExpenseForm
from apps.core.crud import model_form_view, model_delete_view
from apps.tenants.models import Tenant


@login_required
def finance_dashboard(request):
    today = timezone.localdate()
    record_type = request.GET.get("record_type", "all")
    if record_type not in {"all", "invoices", "payments"}:
        record_type = "all"
    search = request.GET.get("q", "").strip()
    tenant_id = request.GET.get("tenant", "")
    status = request.GET.get("status", "")
    date_from = request.GET.get("date_from", "")
    date_to = request.GET.get("date_to", "")

    try:
        parsed_from = date.fromisoformat(date_from) if date_from else None
    except ValueError:
        parsed_from = None
    try:
        parsed_to = date.fromisoformat(date_to) if date_to else None
    except ValueError:
        parsed_to = None

    invoices = Invoice.objects.exclude(status="cancelled")
    payments = Payment.objects.select_related("tenant", "invoice")

    if record_type == "payments":
        invoices = Invoice.objects.none()
    if record_type == "invoices":
        payments = Payment.objects.none()

    if tenant_id:
        invoices = invoices.filter(tenant_id=tenant_id)
        payments = payments.filter(tenant_id=tenant_id)
    if status:
        invoices = invoices.filter(status=status)
    if parsed_from:
        invoices = invoices.filter(issue_date__gte=parsed_from)
        payments = payments.filter(payment_date__gte=parsed_from)
    if parsed_to:
        invoices = invoices.filter(issue_date__lte=parsed_to)
        payments = payments.filter(payment_date__lte=parsed_to)
    if search:
        invoices = invoices.filter(
            Q(invoice_number__icontains=search)
            | Q(description__icontains=search)
            | Q(tenant__full_name__icontains=search)
            | Q(tenant__tenant_id__icontains=search)
        )
        payments = payments.filter(
            Q(receipt_number__icontains=search)
            | Q(reference__icontains=search)
            | Q(invoice__invoice_number__icontains=search)
            | Q(tenant__full_name__icontains=search)
            | Q(tenant__tenant_id__icontains=search)
        )

    invoices = invoices.select_related("tenant", "unit").order_by("-issue_date")
    payments = payments.order_by("-payment_date", "-created_at")
    money_field = DecimalField(max_digits=16, decimal_places=2)
    zero_money = Value(Decimal("0.00"), output_field=money_field)
    invoice_balance = Case(
        When(
            paid_amount__lt=F("amount"),
            then=ExpressionWrapper(
                F("amount") - F("paid_amount"), output_field=money_field
            ),
        ),
        default=zero_money,
        output_field=money_field,
    )

    return render(request,"finance/dashboard.html",{
        "invoices":invoices[:10],
        "payments":payments[:10],
        "total_billed":invoices.aggregate(v=Sum("amount"))["v"] or 0,
        "total_collected":payments.aggregate(v=Sum("amount"))["v"] or 0,
        "expenses":Expense.objects.aggregate(v=Sum("amount"))["v"] or 0,
        "outstanding":invoices.aggregate(
            v=Coalesce(Sum(invoice_balance), zero_money)
        )["v"],
        "today":today,
        "tenants":Tenant.objects.order_by("full_name"),
        "invoice_statuses":Invoice.STATUS,
        "filters":{
            "record_type":record_type,
            "q":search,
            "tenant":tenant_id,
            "status":status,
            "date_from":date_from,
            "date_to":date_to,
        },
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
