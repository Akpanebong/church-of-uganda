from django import template

register = template.Library()

@register.filter
def money(value):
    try:
        return f"UGX {float(value):,.0f}"
    except (TypeError, ValueError):
        return "UGX 0"

@register.filter
def status_class(value):
    value = str(value or "").lower().replace(" ", "-")
    return {"active": "success", "paid": "success", "completed": "success",
            "closed": "success", "high": "danger", "critical": "danger",
            "overdue": "danger", "urgent": "danger", "pending": "warning",
            "open": "warning"}.get(value, "neutral")

@register.simple_tag
def active_nav(request, prefix):
    return "active" if request.path.startswith(prefix) else ""
