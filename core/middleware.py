# core/middleware.py
from django.conf import settings
from django.shortcuts import render
from .models import SiteSettings

class MaintenanceModeMiddleware:
    """
    Show maintenance page when SiteSettings.maintenance_mode is ON.
    - Allows /admin/* (so you can still manage the site)
    - Allows login/logout/password reset
    - Allows /static/* and /media/* (assets)
    - Optional IP and path allow-lists via settings:
        MAINTENANCE_ALLOW_IPS = ['127.0.0.1']
        MAINTENANCE_ALLOW_PATHS = ['/healthz']
    """

    def __init__(self, get_response):
        self.get_response = get_response

        # Always-allowed prefixes (keep CSS/JS/images working + admin access)
        self._default_allowed_prefixes = [
            '/static/',          # static files
            getattr(settings, 'MEDIA_URL', '/media/'),  # media uploads
            '/admin/',           # whole admin (incl. login/logout)
            '/favicon.ico',
        ]

    def __call__(self, request):
        # Dynamic allow-lists from settings.py (optional)
        extra_paths = getattr(settings, "MAINTENANCE_ALLOW_PATHS", [])
        allow_ips = set(getattr(settings, "MAINTENANCE_ALLOW_IPS", []))

        # If request IP is explicitly allowed, skip maintenance
        ip = request.META.get("REMOTE_ADDR")
        if ip in allow_ips:
            return self.get_response(request)

        # Allow specific path prefixes
        path = request.path or '/'
        for prefix in [*self._default_allowed_prefixes, *extra_paths]:
            if prefix and path.startswith(prefix):
                return self.get_response(request)

        # Enforce maintenance if enabled
        ss = SiteSettings.objects.first()
        if ss and ss.maintenance_mode:
            context = {
                "site_settings": ss,
                "maintenance_until": getattr(ss, "maintenance_until", None),
            }
            # Render your maintenance template (ensure path is correct)
            return render(request, "core/maintanance.html", context, status=503)

        # Otherwise continue as normal
        return self.get_response(request)
