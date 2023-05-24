from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    # base template
    path('', views.home_view, name='home_view'),
    # header templates
    path('search/', views.search_form, name='search'),
    path('about/', views.about_view, name='about'),
    path('delivery/', views.delivery_form, name='delivery'),
    path('profile/', views.user_view, name='user_profile'),
    path('support/', views.support_form, name='support'),
    # category
    path('category/', views.parent_category, name='category'),
    path('subcategory/', views.pod_category, name='subcategory'),
    path('category/<slug:category_slug>', views.category_view, name='category_view'),
    # products
    path('<slug:slug>', views.product_detail, name='product_detail'),
    path('novinki/', views.new_products, name='new_products'),
    path('popular/', views.popular_products, name='popular_products'),
    # user
    path('auth/', views.login_user, name='login_user'),
    path('registration/', views.register_user, name='register_user'),
    path('logout/', views.logout_user, name='logout_user'),
]
