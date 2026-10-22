from django.conf import settings
from django.db import models

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class Notification(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=180)
    message = models.TextField()
    url = models.CharField(max_length=300, blank=True)
    is_read = models.BooleanField(default=False)
    priority = models.CharField(max_length=20, default="normal", choices=[("low","Low"),("normal","Normal"),("high","High")])

    def __str__(self):
        return self.title


class AuditLog(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    action = models.CharField(max_length=80)
    model_name = models.CharField(max_length=120)
    object_id = models.CharField(max_length=80, blank=True)
    description = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
    def __str__(self):
        return f"{self.action} {self.model_name} {self.object_id}"


class DioceseProfile(TimeStampedModel):
    """The institutional identity and control dates for the estates manual."""
    church_name = models.CharField(max_length=180, default="Church of Uganda")
    diocese_name = models.CharField(max_length=180, default="Diocese of Madi West Nile")
    department_name = models.CharField(max_length=180, default="Diocesan Estates Department")
    postal_address = models.CharField(max_length=180, default="P.O. Box 370, Arua")
    location = models.CharField(max_length=180, default="Arua, Uganda")
    effective_date = models.DateField(null=True, blank=True)
    review_date = models.DateField(null=True, blank=True)
    approved_by = models.CharField(max_length=180, blank=True)
    approval_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Diocese profile"

    def __str__(self):
        return self.diocese_name

class EstateDocument(TimeStampedModel):
    CATEGORIES = [("title", "Land title"), ("lease", "Lease agreement"),
                  ("plan", "Building plan"), ("report", "Report"),
                  ("policy", "Policy / manual"), ("other", "Other")]
    title = models.CharField(max_length=180)
    category = models.CharField(max_length=30, choices=CATEGORIES, default="other")
    reference = models.CharField(max_length=80, blank=True)
    property = models.ForeignKey("properties.Property", null=True, blank=True,
                                  on_delete=models.SET_NULL, related_name="documents")
    file = models.FileField(upload_to="estate-documents/%Y/%m/", blank=True)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                               on_delete=models.SET_NULL, related_name="estate_documents")
    is_confidential = models.BooleanField(default=False)

    def __str__(self):
        return self.title
