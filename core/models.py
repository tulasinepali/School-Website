# app: core_settings/models.py
from django.db import models
from django.core.validators import FileExtensionValidator, RegexValidator

HEX_COLOR_VALIDATOR = RegexValidator(
    regex=r"^#(?:[0-9a-fA-F]{3}){1,2}$",
    message="Enter a valid hex color like #004aad",
)

class SiteSettings(models.Model):
    # ---- Singleton enforcer (only one instance allowed) ----
    singleton_enforcer = models.BooleanField(
        default=True, unique=True, editable=False,
        help_text="Prevents creating more than one settings row."
    )
    maintenance_mode = models.BooleanField(default=False)
    maintenance_message = models.TextField(blank=True)
    maintenance_until = models.DateTimeField(null=True, blank=True)
    # ---- Site Information ----
    site_title = models.CharField(max_length=120, default="EduStage Academy")
    tagline = models.CharField(max_length=160, blank=True)
    base_url = models.URLField(blank=True, help_text="e.g. https://myschool.edu.np")
    contact_email = models.EmailField(blank=True)
    default_language = models.CharField(max_length=40, default="en")
    timezone = models.CharField(max_length=60, default="Asia/Kathmandu")
    date_format = models.CharField(max_length=32, default="DD/MM/YYYY")
    currency = models.CharField(max_length=8, default="NPR")
    maintenance_mode = models.BooleanField(default=False)

    # ---- Branding & Favicon ----
    favicon = models.ImageField(
        upload_to="static/branding/",
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=["ico", "png"])],
        help_text="Upload .ico or .png",
    )
    logo_light = models.ImageField(upload_to="static/branding/", blank=True)
    logo_dark  = models.ImageField(upload_to="static/branding/", blank=True)
    logo_mobile = models.ImageField(upload_to="static/branding/", blank=True)
    app_icon_pwa = models.ImageField(
        upload_to="branding/",
        blank=True,
        help_text="512x512 PNG recommended for PWA"
    )

    theme_primary_color = models.CharField(
        max_length=7, default="#004aad", validators=[HEX_COLOR_VALIDATOR]
    )
    font_family = models.CharField(max_length=80, default="Rubik")

    # Social links as simple URLs (keep optional)
    facebook_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)

    # ---- Display & SEO ----
    homepage_title_meta = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    meta_keywords = models.CharField(
        max_length=250, blank=True,
        help_text="Comma-separated (optional)"
    )
    og_image = models.ImageField(upload_to="seo/", blank=True)
    analytics_id = models.CharField(
        max_length=40, blank=True, help_text="GA4 / GTM / etc."
    )

    # ---- System & Admin ----
    admin_email = models.EmailField(blank=True)
    error_reporting_enabled = models.BooleanField(default=True)

    BACKUP_CHOICES = [
        ("never", "Never"),
        ("daily", "Daily"),
        ("weekly", "Weekly"),
        ("monthly", "Monthly"),
    ]
    backup_frequency = models.CharField(
        max_length=10, choices=BACKUP_CHOICES, default="weekly"
    )

    version_info = models.CharField(
        max_length=40, blank=True, help_text="Read-only or filled by releases."
    )

    # ---- Timestamps ----
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ---- Convenience ----
    def __str__(self):
        return "Site Settings"

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"
