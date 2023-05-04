from django.shortcuts import render

# Create your views here.
from .models import Category, Product, Popular_product, Newest_product


def all_products(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products', products})