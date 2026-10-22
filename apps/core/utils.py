from .models import AuditLog, Notification
from django.utils.text import slugify

def audit(user, action, obj, description="", request=None):
    return AuditLog.objects.create(
        user=user if getattr(user, "is_authenticated", False) else None,
        action=action,
        model_name=obj.__class__.__name__,
        object_id=str(getattr(obj, "pk", "")),
        description=description,
        ip_address=request.META.get("REMOTE_ADDR") if request else None,
    )

def notify(user, title, message, url=""):
    return Notification.objects.create(user=user, title=title, message=message, url=url)

def money(value):
    return f"UGX {value:,.0f}"

def generate_reference(prefix, model, field="reference"):
    """Generate a human-readable register reference without relying on database IDs."""
    number = model.objects.count() + 1
    candidate = f"{prefix}-{number:04d}"
    while model.objects.filter(**{field: candidate}).exists():
        number += 1
        candidate = f"{prefix}-{number:04d}"
    return candidate

def normalize_search(value):
    return " ".join((value or "").strip().split())
