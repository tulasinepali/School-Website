from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db import models
from django import forms

from .models import (
    HomePage,
    FeatureItem,
    LeadershipMessage,
    StatItem,
    Testimonial,
    PartnerLogo,
    HeroSlide,
    EventSnippet,
    Announcement,
)

# ------------------------------------------------------------
# Small reusable helpers
# ------------------------------------------------------------
class ReadonlyThumbMixin:
    """Add a tiny image preview in admin (read-only)."""
    thumb_fields = {"photo", "logo", "image", "banner", "hero_background"}

    def thumb(self, obj):
        if not obj or not getattr(obj, "pk", None):
            return "-"
        for f in self.thumb_fields:
            if hasattr(obj, f):
                file = getattr(obj, f)
                if file and getattr(file, "url", None):
                    return mark_safe(
                        f'<img src="{file.url}" style="height:48px;border-radius:6px;object-fit:cover;">'
                    )
        return "-"

    thumb.short_description = "Preview"


# ------------------------------------------------------------
# Inline base configuration
# ------------------------------------------------------------
class BaseTabularInline(admin.TabularInline, ReadonlyThumbMixin):
    extra = 0
    show_change_link = True
    # classes = ("collapse",)
    readonly_fields = ("thumb",)
    ordering = ("order", "id")


class BaseStackedInline(admin.StackedInline, ReadonlyThumbMixin):
    extra = 0
    show_change_link = True
    # classes = ("collapse",)
    readonly_fields = ("thumb",)
    ordering = ("order", "id")


# ------------------------------------------------------------
# Inlines for all homepage child models
# ------------------------------------------------------------
class FeatureItemInline(BaseTabularInline):
    model = FeatureItem
    fields = ("is_active", "order", "icon_class", "title", "description")


class LeadershipMessageInline(BaseStackedInline):
    model = LeadershipMessage
    fields = (
        "is_active", "order", "role", "align",
        "name", "title_line", "photo", "thumb",
        "message", "profile_link",
    )


class StatItemInline(BaseTabularInline):
    model = StatItem
    fields = ("is_active", "order", "label", "value", "suffix")


class TestimonialInline(BaseStackedInline):
    model = Testimonial
    fields = ("is_active", "order", "name", "role", "photo", "thumb", "quote")


class PartnerLogoInline(BaseTabularInline):
    model = PartnerLogo
    fields = ("is_active", "order", "name", "logo", "thumb", "url")


class HeroSlideInline(BaseStackedInline):
    model = HeroSlide
    fields = ("is_active", "order", "image", "thumb", "headline", "subheadline", "cta_text", "cta_url")


class EventSnippetInline(BaseStackedInline):
    model = EventSnippet
    fields = ("is_active", "order", "title", "date_text", "location", "link", "banner", "thumb")


class AnnouncementInline(admin.StackedInline):
    model = Announcement
    can_delete = True
    max_num = 1
    extra = 0
    fields = ("enabled", "text", "url", ("start_at", "end_at"))


# ------------------------------------------------------------
# HomePage Admin (singleton)
# ------------------------------------------------------------
@admin.register(HomePage)
class HomePageAdmin(admin.ModelAdmin, ReadonlyThumbMixin):
    """Main homepage content editor with all sections inline."""

    formfield_overrides = {
        models.TextField: {"widget": forms.Textarea(attrs={"rows": 4})},
        models.CharField: {"widget": forms.TextInput(attrs={"style": "max-width:520px"})},
    }

    fieldsets = (
        ("Hero Section", {
            "fields": (
                "hero_title", "hero_subtitle", "hero_background", "thumb",
                ("hero_cta_text", "hero_cta_url"),
            )
        }),
        ("Section Toggles", {
            "fields": (
                "show_features", "show_stats", "show_leadership",
                "show_testimonials", "show_partners", "show_events",
            )
        }),
        ("SEO / Open Graph", {
            "fields": ("seo_title", "seo_description", "og_image"),
            # "classes": ("collapse",)
        }),
    )

    readonly_fields = ("thumb",)

    inlines = [
        AnnouncementInline,
        FeatureItemInline,
        LeadershipMessageInline,
        StatItemInline,
        TestimonialInline,
        PartnerLogoInline,
        HeroSlideInline,
        EventSnippetInline,
    ]

    # Singleton protection
    def has_add_permission(self, request):
        return not HomePage.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        """Redirect the list view directly to the single instance edit page."""
        try:
            obj = HomePage.objects.get()
            return HttpResponseRedirect(
                reverse("admin:homepage_homepage_change", args=[obj.pk])
            )
        except HomePage.DoesNotExist:
            return HttpResponseRedirect(reverse("admin:homepage_homepage_add"))


# ------------------------------------------------------------
# Optional: Direct model admins (for separate editing)
# ------------------------------------------------------------
class HiddenFromIndex(admin.ModelAdmin):
    """Hide from sidebar but allow inline editing."""
    def get_model_perms(self, request):
        return {}


@admin.register(FeatureItem)
class FeatureItemAdmin(HiddenFromIndex):
    list_display = ("title", "order", "is_active", "homepage")
    list_editable = ("order", "is_active")
    list_filter = ("is_active",)
    search_fields = ("title", "description")


@admin.register(LeadershipMessage)
class LeadershipMessageAdmin(HiddenFromIndex):
    list_display = ("name", "role", "align", "order", "is_active", "homepage")
    list_editable = ("order", "is_active", "align")
    list_filter = ("role", "align", "is_active")
    search_fields = ("name", "title_line", "message")


@admin.register(StatItem)
class StatItemAdmin(HiddenFromIndex):
    list_display = ("label", "value", "suffix", "order", "is_active", "homepage")
    list_editable = ("order", "is_active")


@admin.register(Testimonial)
class TestimonialAdmin(HiddenFromIndex):
    list_display = ("name", "role", "order", "is_active", "homepage")
    list_editable = ("order", "is_active")
    search_fields = ("name", "role", "quote")


@admin.register(PartnerLogo)
class PartnerLogoAdmin(HiddenFromIndex, ReadonlyThumbMixin):
    list_display = ("name", "order", "is_active", "homepage", "thumb")
    list_editable = ("order", "is_active")


@admin.register(HeroSlide)
class HeroSlideAdmin(HiddenFromIndex, ReadonlyThumbMixin):
    list_display = ("headline", "order", "is_active", "homepage", "thumb")
    list_editable = ("order", "is_active")


@admin.register(EventSnippet)
class EventSnippetAdmin(HiddenFromIndex, ReadonlyThumbMixin):
    list_display = ("title", "date_text", "location", "order", "is_active", "homepage", "thumb")
    list_editable = ("order", "is_active")


@admin.register(Announcement)
class AnnouncementAdmin(HiddenFromIndex):
    list_display = ("enabled", "text", "start_at", "end_at", "homepage")
    list_filter = ("enabled",)
