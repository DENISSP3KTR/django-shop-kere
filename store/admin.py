from django.contrib import admin
from django import forms
from mptt.admin import MPTTModelAdmin
# Register your models here.

from .models import *

# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ['name', 'slug', 'image']
#     prepopulated_fields = {'slug': ('name',)}
#     search_fields = ('name',)

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone_number', 'create_time']
    search_fields = ('name',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['client', 'product', 'quantity', 'price', 'address', 'date_ordered', 'is_completed']
    search_fields = ('client',)

@admin.register(Popular_product)
class Popular_productAdmin(admin.ModelAdmin):
    list_display = ['popular_product', 'start_date', 'end_date']

@admin.register(Newest_product)
class Newest_productAdmin(admin.ModelAdmin):
    list_display = ['new_product', 'start_date', 'end_date']

@admin.register(Sale_product)
class sale_productAdmin(admin.ModelAdmin):
    list_display = ['sale_product']

class ProductImageAdmin(admin.ModelAdmin):
  pass

class ProductImageInline(admin.StackedInline):
  model = ProductImage
  max_num = 10
  extra = 0

class ProductAdmin(admin.ModelAdmin):
  list_display = ['name', 'description', 'price', 'amount1', 'amount2', 'stock', 'category', 'created_time', 'update', 'discount']
  prepopulated_fields = {'slug': ('name',)}
  inlines = [ProductImageInline,]

admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(Product, ProductAdmin)

# class PodCategoryAdmin(admin.ModelAdmin):
#    pass

# class PodCategoryInline(admin.TabularInline):
#    prepopulated_fields = {'slug': ('name',)}
#    model = PodCategory
#    max_num = 10
#    extra = 0

# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ['name', 'slug', 'image']
#     prepopulated_fields = {'slug': ('name',)}
#     search_fields = ('name',)
#     inlines = [PodCategoryInline,]

# admin.site.register(PodCategory, PodCategoryAdmin)
# admin.site.register(Category, CategoryAdmin)

class CategoryAdmin(MPTTModelAdmin):
    list_display = ['name', 'slug', 'image']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)