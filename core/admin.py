from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import SiteSettings

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    readonly_fields = ("singleton_enforcer",)
    
    fieldsets = (
        ("Site Information", {
            "fields": (
                "site_title", "tagline", "base_url", "contact_email",
                "default_language", "timezone", "date_format",
                "currency", "maintenance_mode",
            )
        }),
        ("Branding & Favicon", {
            "fields": (
                "favicon", "logo_light", "logo_dark", "logo_mobile",
                "app_icon_pwa", "theme_primary_color", "font_family",
                "facebook_url", "youtube_url", "instagram_url", "linkedin_url",
            )
        }),
        ("Display & SEO", {
            "fields": (
                "homepage_title_meta", "meta_description",
                "meta_keywords", "og_image", "analytics_id",
            )
        }),
        ("System & Admin", {
            "fields": (
                "admin_email", "error_reporting_enabled",
                "backup_frequency", "version_info",
            )
        }),
    )

    # --- Hide delete, prevent multiple records ---
    def has_add_permission(self, request): return not SiteSettings.objects.exists()
    def has_delete_permission(self, request, obj=None): return False

    def changelist_view(self, request, extra_context=None):
        from django.urls import reverse
        from django.http import HttpResponseRedirect
        from .models import SiteSettings
        try:
            obj = SiteSettings.objects.get()
            return HttpResponseRedirect(reverse("admin:core_sitesettings_change", args=[obj.id]))
        except SiteSettings.DoesNotExist:
            from django.urls import reverse
            return HttpResponseRedirect(reverse("admin:core_sitesettings_add"))
