from django.db import models
from apps.core.models import TimeStampedModel
from apps.tenants.models import Tenant
from apps.properties.models import Unit, Property


class Invoice(TimeStampedModel):
    STATUS=[("unpaid","Unpaid"),("partial","Partially Paid"),("paid","Paid"),("overdue","Overdue"),("cancelled","Cancelled")]
    invoice_number=models.CharField(max_length=40,unique=True)
    tenant=models.ForeignKey(Tenant,on_delete=models.PROTECT,related_name="invoices")
    unit=models.ForeignKey(Unit,null=True,blank=True,on_delete=models.SET_NULL,related_name="invoices")
    issue_date=models.DateField()
    due_date=models.DateField()
    description=models.CharField(max_length=240)
    amount=models.DecimalField(max_digits=14,decimal_places=2)
    paid_amount=models.DecimalField(max_digits=14,decimal_places=2,default=0)
    status=models.CharField(max_length=20,choices=STATUS,default="unpaid")
    lease=models.OneToOneField("leases.Lease", null=True, blank=True, on_delete=models.SET_NULL, related_name="invoice")

    @property
    def balance(self):
        return max(self.amount-self.paid_amount,0)


class Payment(TimeStampedModel):
    METHODS=[("cash","Cash"),("bank","Bank Transfer"),("mobile","Mobile Money"),("card","Card"),("cheque","Cheque")]
    receipt_number=models.CharField(max_length=40,unique=True)
    tenant=models.ForeignKey(Tenant,on_delete=models.PROTECT,related_name="payments")
    invoice=models.ForeignKey(Invoice,null=True,blank=True,on_delete=models.SET_NULL,related_name="payments")
    payment_date=models.DateField()
    amount=models.DecimalField(max_digits=14,decimal_places=2)
    method=models.CharField(max_length=20,choices=METHODS)
    reference=models.CharField(max_length=100,blank=True)
    notes=models.TextField(blank=True)


class Expense(TimeStampedModel):
    CATEGORIES=[("maintenance","Maintenance"),("utilities","Utilities"),("security","Security"),("cleaning","Cleaning"),("staff","Staff"),("tax","Tax"),("insurance","Insurance"),("other","Other")]
    property=models.ForeignKey(Property,null=True,blank=True,on_delete=models.SET_NULL,related_name="expenses")
    category=models.CharField(max_length=30,choices=CATEGORIES)
    description=models.CharField(max_length=240)
    amount=models.DecimalField(max_digits=14,decimal_places=2)
    expense_date=models.DateField()
    vendor=models.CharField(max_length=180,blank=True)
    reference=models.CharField(max_length=100,blank=True)
