from .models import Notification, DioceseProfile
def enterprise_context(request):
    unread = Notification.objects.filter(user=request.user, is_read=False).count() if request.user.is_authenticated else 0
    profile = DioceseProfile.objects.filter(is_active=True).first()
    return {"unread_notifications": unread, "app_name": "Diocesan Estates Management",
            "app_tagline": "Church of Uganda · Diocese of Madi West Nile",
            "diocese_profile": profile}
