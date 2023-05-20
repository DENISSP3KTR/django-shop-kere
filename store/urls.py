from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    # base template
    path('', views.home_view, name='home_view'),
    # header templates
    path('search', views.search_form, name='search_form'),
    path('about', views.about_form, name='about_form'),
    path('delivery', views.delivery_form, name='delivery_form'),
    path('user_profile', views.user_form, name='user_form'),
    path('support', views.support_form, name='support_form'),
    # category
    path('category', views.all_categories, name='all_categories'),
    # products
]
