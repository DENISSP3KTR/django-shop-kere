from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout, authenticate, login, get_user_model
from django.views.generic import TemplateView
# Create your views here.
from .models import *

from store import forms
# header templates
def about_view(request):
    return render(request, 'store/headertemplates/about.html')

def search_form(request):
    return render(request, 'store/headertemplates/search.html')

def delivery_form(request):
    return render(request, 'store/headertemplates/delivery.html')

def support_form(request):
    return render(request, 'store/headertemplates/support.html')



# products
def all_products(request):
    product = Product.objects.all()
    return render(request, 'store/products/product.html', {"product": product})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, stock=True)
    return render(request, 'store/products/product_detail.html', {'product': product})

def new_products(request):
    product = Newest_product.objects.all()
    return render(request, 'store/products/new_product.html', {"product": product})

def popular_products(request):
    product = Popular_product.objects.all()
    return render(request, 'store/products/popular_product.html', {"product": product})

# category
def parent_category(request):
    categories = Category.objects.filter(parent__isnull=True)
    return render(request, 'store/category/category.html', {"categories": categories})

def pod_category(request):
    podcat = Category.objects.filter(parent__isnull=False)
    return render(request, 'store/category/pod_category.html', {"podcat": podcat})

def category_view(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    if category.get_descendants().exists():
        context = {
            'category': category,
        }
        return render(request, 'store/category/pod_category.html', context)
    else:
        context = {
            'category': category,
            'product': category.products.all(),
        }
        return render(request, 'store/products/product.html', context)
    



# base templates
def home_view(request):
    categories = Category.objects.filter(parent__isnull=True)
    new_product = Newest_product.objects.all()
    popular_product = Popular_product.objects.all()
    context = {
        'new_product': new_product,
        'categories': categories,
        'popular_product': popular_product,
    }
    return render(request, 'store/home.html', context)


# user

def login_user(request):
    context = {
        'login_form': forms.LoginForm()
    }
    if request.method == 'POST':
        login_form = forms.LoginForm(request.POST)
        if login_form.is_valid():
            email = login_form.cleaned_data['email']
            password = login_form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect('/')
            else:
                context = {
                    'login_form': forms.LoginForm(request.POST),
                    'attention': f'Неправильно введены данные!',
                }
    return render(request, 'store/client/login.html', context)

def register_user(request):
    context = {
        'register_form': forms.RegisterForm()
    }
    User = get_user_model()
    if request.method == 'POST':
        register_form = forms.RegisterForm(request.POST)
        if register_form.is_valid():
            user = User.objects.create_user(
                username = register_form.cleaned_data['email'],
                password = register_form.cleaned_data['password']
            )
            user.email = register_form.cleaned_data['email']
            user.last_name = register_form.cleaned_data['last_name']
            user.first_name = register_form.cleaned_data['first_name']
            user.patronymic = register_form.cleaned_data['patronymic']
            user.phone_number = register_form.cleaned_data['phone_number']
            user.save()
            user.set_password(user.password)
            user.save()
            return redirect('login_user')
        else:
            context = {
                'register_form': forms.RegisterForm()
            }
    return render(request, 'store/client/register.html', context)

def logout_user(request):
    logout(request)
    return redirect('/')

def user_view(request):
    return render(request, 'store/client/user_profile.html')