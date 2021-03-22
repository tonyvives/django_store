from .models import Category


def all_categories(request):
    nav_categories = Category.objects.all()
    return {"nav_categories": nav_categories}
