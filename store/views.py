from django.shortcuts import render

# Create your views here.
from .models import *


# header templates
def about_form(request):
    return render(request, 'store/headertemplates/about.html')

def search_form(request):
    return render(request, 'store/headertemplates/search.html')

def delivery_form(request):
    return render(request, 'store/headertemplates/delivery.html')

def support_form(request):
    return render(request, 'store/headertemplates/support.html')

def user_form(request):
    return render(request, 'store/headertemplates/user_profile.html')

# products
def all_products(request):
    product = Product.objects.filter()
    return render(request, 'store/products/product.html', {"product": product})

# category
def all_categories(request):
    categories = Category.objects.filter(parent__isnull=True)
    return render(request, 'store/category/category.html', {"categories": categories})

# base templates
def home_view(request):
    categories = Category.objects.filter(parent__isnull=True)
    new_product = Newest_product.objects.all()
    popular_product = Popular_product.objects.all()
    context = {
        'new_product': new_product,
        'categories': categories,
        'popular_product': popular_product
    }
    return render(request, 'store/home.html', context)
