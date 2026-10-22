from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.properties.models import Property, Building, Unit
from apps.tenants.models import Tenant, TenantUnit
from apps.leases.models import Lease
from apps.finance.models import Invoice, Payment
from apps.maintenance.models import MaintenanceRequest

class Command(BaseCommand):
    help = "Create demo estate data."
    def handle(self,*args,**kwargs):
        User=get_user_model()
        user,_=User.objects.get_or_create(username="admin",defaults={"email":"admin@example.com","is_staff":True,"is_superuser":True})
        if not user.has_usable_password(): user.set_password("ChangeMe123!"); user.save()
        p,_=Property.objects.get_or_create(code="EST-001",defaults={
            "name":"Green Valley Residences","property_type":"residential",
            "address":"Kampala, Uganda","city":"Kampala","owner_name":"EstatePro Holdings",
            "description":"Premium managed residential estate."
        })
        b,_=Building.objects.get_or_create(property=p,name="Block A",defaults={"floors":4})
        units=[]
        for n,rent,status in [("A101",1200000,"occupied"),("A102",1250000,"available"),("A201",1400000,"occupied"),("A202",1450000,"maintenance")]:
            u,_=Unit.objects.get_or_create(property=p,unit_number=n,defaults={"building":b,"unit_type":"2 Bedroom","bedrooms":2,"bathrooms":2,"monthly_rent":rent,"service_charge":100000,"status":status})
            units.append(u)
        t,_=Tenant.objects.get_or_create(tenant_id="TEN-0001",defaults={"full_name":"Daniel Okello","phone":"+256 700 000 001","email":"daniel@example.com"})
        TenantUnit.objects.get_or_create(tenant=t,unit=units[0],defaults={"move_in":date.today()-timedelta(days=180)})
        l,_=Lease.objects.get_or_create(lease_number="LSE-0001",defaults={"tenant":t,"unit":units[0],"start_date":date.today()-timedelta(days=180),"end_date":date.today()+timedelta(days=185),"rent":1200000,"deposit":2400000,"service_charge":100000,"status":"active"})
        inv,_=Invoice.objects.get_or_create(invoice_number="INV-0001",defaults={"tenant":t,"unit":units[0],"issue_date":date.today(),"due_date":date.today()+timedelta(days=7),"description":"Monthly Rent — Demo","amount":1300000,"paid_amount":500000,"status":"partial"})
        Payment.objects.get_or_create(receipt_number="RCT-0001",defaults={"tenant":t,"invoice":inv,"payment_date":date.today(),"amount":500000,"method":"mobile","reference":"DEMO-MOMO"})
        MaintenanceRequest.objects.get_or_create(request_number="MNT-0001",defaults={"unit":units[3],"reported_by":user,"category":"Plumbing","description":"Demo maintenance request for bathroom plumbing.","priority":"high","status":"assigned","assigned_to":"Maintenance Team"})
        self.stdout.write(self.style.SUCCESS("Demo data created. Login: admin / ChangeMe123!"))
