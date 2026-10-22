from django.urls import path
from .views import finance_dashboard, invoice_create, invoice_update, invoice_delete, payment_create, payment_update, payment_delete, expense_create, expense_update, expense_delete

urlpatterns=[
    path("",finance_dashboard,name="finance_d"),
    path("invoices/new/",invoice_create,name="invoice_create"),
    path("invoices/<int:pk>/edit/",invoice_update,name="invoice_update"),
    path("invoices/<int:pk>/delete/",invoice_delete,name="invoice_delete"),
    path("payments/new/",payment_create,name="payment_create"),
    path("payments/<int:pk>/edit/",payment_update,name="payment_update"),
    path("payments/<int:pk>/delete/",payment_delete,name="payment_delete"),
    path("expenses/new/",expense_create,name="expense_create"),
    path("expenses/<int:pk>/edit/",expense_update,name="expense_update"),
    path("expenses/<int:pk>/delete/",expense_delete,name="expense_delete"),
]
