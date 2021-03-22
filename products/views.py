from django.shortcuts import render
from .models import Product, Category


def home(request, category_slug=None):
    if category_slug != None:
        category_page = Category.objects.get(slug=category_slug)
        products = Product.objects.filter(category=category_page, available=True)
    else:
        category_page = None
        products = Product.objects.all()
    context = {"products": products, "category_page": category_page}
    return render(request, "products/home.html", context)


def product(request, category_slug, product_slug):
    product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    context = {"product": product}
    return render(request, "products/product.html", context)


def search(request):
    products = Product.objects.filter(name__contains=request.GET["name"])
    context = {"products": products}
    return render(request, "products/home.html", context)
