from django.db import models
from django.core.validators import URLValidator, RegexValidator

# ---------- Helpers ----------
HEX_COLOR_VALIDATOR = RegexValidator(
    regex=r"^#(?:[0-9a-fA-F]{3}){1,2}$",
    message="Enter a valid hex color like #004aad"
)


# ---------- HomePage (Singleton) ----------
class HomePage(models.Model):
    """Stores all homepage settings and content."""
    singleton_enforcer = models.BooleanField(default=True, unique=True, editable=False)


    # Hero section
    hero_title = models.CharField(max_length=160, default="Welcome to Our School")
    hero_subtitle = models.CharField(max_length=220, blank=True, default="Learn • Grow • Achieve")
    hero_background = models.ImageField(upload_to="static/homepage/hero/", blank=True)
    hero_cta_text = models.CharField(max_length=40, blank=True, default="Get Started")
    hero_cta_url = models.CharField(max_length=255, blank=True, validators=[URLValidator()])

    # Visibility toggles
    show_features = models.BooleanField(default=True)
    show_stats = models.BooleanField(default=True)
    show_leadership = models.BooleanField(default=True)
    show_testimonials = models.BooleanField(default=True)
    show_partners = models.BooleanField(default=True)
    show_events = models.BooleanField(default=True)

    # SEO / Social
    seo_title = models.CharField(max_length=70, blank=True)
    seo_description = models.CharField(max_length=160, blank=True)
    og_image = models.ImageField(upload_to="static/homepage/og/", blank=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Homepage"
        verbose_name_plural = "Homepage"

    def __str__(self):
        return "Homepage"

    # Safe singleton save method
    def save(self, *args, **kwargs):
        existing = HomePage.objects.first()
        if existing and not self.pk:
            self.pk = existing.pk  # Always update instead of blocking
        super().save(*args, **kwargs)
class Orderable(models.Model):
    """Adds order & active fields to related homepage items."""
    order = models.PositiveIntegerField(default=0, help_text="Lower appears first")
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ["order", "id"]
class FeatureItem(Orderable):
    homepage = models.ForeignKey(HomePage, on_delete=models.CASCADE, related_name="features")
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True)
    icon_class = models.CharField(
        max_length=64, blank=True,
        help_text="e.g. 'fa fa-graduation-cap' or 'ti-light-bulb'"
    )

    def __str__(self):
        return self.title
class LeadershipMessage(Orderable):
    ROLE_CHOICES = [
        ("principal", "Principal"),
        ("chairperson", "Chairperson"),
        ("director", "Director"),
    ]
    ALIGN_CHOICES = [
        ("left", "Image Left"),
        ("right", "Image Right"),
    ]

    homepage = models.ForeignKey(HomePage, on_delete=models.CASCADE, related_name="leadership_messages")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="principal")
    name = models.CharField(max_length=120)
    title_line = models.CharField(max_length=150, blank=True)
    photo = models.ImageField(upload_to="static/homepage/leadership/", blank=True)
    message = models.TextField(blank=True)
    profile_link = models.URLField(blank=True)
    align = models.CharField(max_length=10, choices=ALIGN_CHOICES, default="right")

    def __str__(self):
        return f"{self.get_role_display()}: {self.name}"
class StatItem(Orderable):
    homepage = models.ForeignKey(HomePage, on_delete=models.CASCADE, related_name="stats")
    label = models.CharField(max_length=80)
    value = models.CharField(max_length=32, help_text="Number or short text (e.g., 1.2K)")
    suffix = models.CharField(max_length=12, blank=True, help_text="Optional suffix like %, +, yrs")

    def __str__(self):
        return f"{self.value}{self.suffix} {self.label}"
class Testimonial(Orderable):
    homepage = models.ForeignKey(HomePage, on_delete=models.CASCADE, related_name="testimonials")
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=120, blank=True)
    photo = models.ImageField(upload_to="static/homepage/testimonials/", blank=True)
    quote = models.TextField()

    def __str__(self):
        return f"{self.name} – {self.role or 'Testimonial'}"
class PartnerLogo(Orderable):
    homepage = models.ForeignKey(HomePage, on_delete=models.CASCADE, related_name="partners")
    name = models.CharField(max_length=120)
    logo = models.ImageField(upload_to="static/homepage/partners/")
    url = models.URLField(blank=True)

    def __str__(self):
        return self.name
class HeroSlide(Orderable):
    homepage = models.ForeignKey(HomePage, on_delete=models.CASCADE, related_name="hero_slides")
    image = models.ImageField(upload_to="static/homepage/hero/slides/")
    headline = models.CharField(max_length=160, blank=True)
    subheadline = models.CharField(max_length=220, blank=True)
    cta_text = models.CharField(max_length=40, blank=True)
    cta_url = models.CharField(max_length=255, blank=True, validators=[URLValidator()])

    def __str__(self):
        return self.headline or f"Slide {self.order}"
class EventSnippet(Orderable):
    homepage = models.ForeignKey(HomePage, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=160)
    date_text = models.CharField(max_length=60, blank=True, help_text="e.g., 12 Dec, 3:00 PM")
    location = models.CharField(max_length=120, blank=True)
    link = models.URLField(blank=True)
    banner = models.ImageField(upload_to="static/homepage/events/", blank=True)

    def __str__(self):
        return self.title
class Announcement(models.Model):
    homepage = models.OneToOneField(HomePage, on_delete=models.CASCADE, related_name="announcement")
    enabled = models.BooleanField(default=False)
    text = models.CharField(max_length=160, blank=True)
    url = models.URLField(blank=True)
    start_at = models.DateTimeField(null=True, blank=True)
    end_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Announcement Bar"
        verbose_name_plural = "Announcement Bar"

    def __str__(self):
        return "Homepage Announcement"
