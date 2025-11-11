from .models import SiteSettings

def site_settings(request):
    """
    Adds the SiteSettings instance to all templates as `site_settings`.
    """
    try:
        settings_obj = SiteSettings.objects.first()
    except SiteSettings.DoesNotExist:
        settings_obj = None
    return {'site_settings': settings_obj}
