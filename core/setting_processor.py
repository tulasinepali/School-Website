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
def staff_members(request):
    return {'staff_members': StaffMember.objects.filter(is_active=True).order_by('order')}

