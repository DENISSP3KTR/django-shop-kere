from django.shortcuts import render

# Create your views here.
from .models import *


def all_products(request):
    product = Product.objects.all()
    return render(request, 'store/home.html', {"product": product})


def search_form(request):
    return render(request, 'store/search.html')