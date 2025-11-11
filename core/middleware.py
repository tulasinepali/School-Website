# core/middleware.py
from django.conf import settings
from django.utils import timezone
from django.shortcuts import render
from .models import SiteSettings

# Optional in settings.py:
# MAINTENANCE_ALLOW_PATHS = ['/admin/login/', '/admin/logout/', '/admin/password_reset/']
# MAINTENANCE_ALLOW_IPS = ['127.0.0.1']

class MaintenanceModeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        allow_paths = getattr(settings, "MAINTENANCE_ALLOW_PATHS", ['/admin/login/', '/admin/'])
        allow_ips = set(getattr(settings, "MAINTENANCE_ALLOW_IPS", []))

        # Always allow admin/staff
        if request.user.is_authenticated and request.user.is_staff:
            return self.get_response(request)

        # Allow specific paths (login, etc.)
        for p in allow_paths:
            if request.path.startswith(p):
                return self.get_response(request)

        # Allow specific IPs
        ip = request.META.get("REMOTE_ADDR")
        if ip in allow_ips:
            return self.get_response(request)

        # Enforce maintenance
        ss = SiteSettings.objects.first()
        if ss and ss.maintenance_mode:
            # Pass data to template (including countdown target)
            context = {"site_settings": ss, "maintenance_until": ss.maintenance_until}
            return render(request, "maintenance.html", context, status=503)

        return self.get_response(request)
