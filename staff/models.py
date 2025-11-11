from django.db import models
from django.core.validators import URLValidator

class StaffMember(models.Model):
    """Simple model for teacher/staff profiles shown on the website."""

    name = models.CharField(max_length=120)
    subject_taught = models.CharField(max_length=120, help_text="e.g., Mathematics, Science, English")
    photo = models.ImageField(upload_to="staff/photos/", blank=True)
    short_bio = models.TextField(max_length=400, help_text="A short introduction or biography.", blank=True)

    # Social links (optional)
    facebook = models.URLField(blank=True, validators=[URLValidator()])
    twitter = models.URLField(blank=True, validators=[URLValidator()])
    linkedin = models.URLField(blank=True, validators=[URLValidator()])
    instagram = models.URLField(blank=True, validators=[URLValidator()])

    is_active = models.BooleanField(default=True, help_text="Uncheck to hide from the website.")
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers appear first.")

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Teachers/Staffs"
        verbose_name_plural = "Teacher/Staff"

    def __str__(self):
        return self.name
