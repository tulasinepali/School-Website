from .models import SiteSettings
from staff.models import StaffMember

def site_settings(request):
    """
    Adds the SiteSettings instance to all templates as `site_settings`.
    """
    try:
        settings_obj = SiteSettings.objects.first()
    except SiteSettings.DoesNotExist:
        settings_obj = None
    return {'site_settings': settings_obj}


# staff/context_processors.py
# core/setting_processor.py

def staff_members(request):
    """Add all staff members to templates as `staff_members`."""
    try:
        members = StaffMember.objects.filter(is_active=True).order_by("order")
    except Exception:
        members = []
    return {'staff_members': members}
