from django.shortcuts import render
from homepage.models import HomePage


# Create your views here.
def home(request):
    homepage, created = HomePage.objects.get_or_create(
        singleton_enforcer=True,
        defaults={
            "hero_title": "Welcome to Our School",
            "hero_subtitle": "Learn • Grow • Achieve",
        },
    )

    context = {
        "homepage": homepage,
        "features": homepage.features.filter(is_active=True),
        "stats": homepage.stats.filter(is_active=True),
        "leadership_messages": homepage.leadership_messages.filter(is_active=True),
        "testimonials": homepage.testimonials.filter(is_active=True),
        "partners": homepage.partners.filter(is_active=True),
        "hero_slides": homepage.hero_slides.filter(is_active=True),
        "events": homepage.events.filter(is_active=True),
        "announcement": getattr(homepage, "announcement", None),
    }
   
    return render(request, 'core/index.html',context)

def maintenance_preview(request):
    return render(request, "core/maintanance.html")


