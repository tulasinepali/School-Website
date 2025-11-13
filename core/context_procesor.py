from homepage.models import HomePage

def global_homepage(request):
    """
    Provides a global HomePage singleton object to all templates.
    """
    homepage = HomePage.objects.first()
    if not homepage:
        homepage = HomePage.objects.create()  # auto enforces singleton

    return {
        "G_HOMEPAGE": homepage
    }
