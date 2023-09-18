from django.contrib import admin
from django import forms


from mptt.admin import MPTTModelAdmin
# Register your models here.

from .models import *

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'patronymic', 'email', 'phone_number', 'date_joined']

@admin.register(OrderStatus)
class OrderStatusAdmin(admin.ModelAdmin):
   pass

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['client', 'status', 'delivery_parametr', 'address', 'date_ordered', 'is_completed']
    search_fields = ('client', 'status')

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

class ProductСharacteristicAdmin(admin.ModelAdmin):
  pass

class ProductCharacterInline(admin.StackedInline):
  model = Сharacteristic

class ProductAdmin(admin.ModelAdmin):
  list_display = ['id', 'name', 'description', 'price', 'amount1', 'stock', 'category', 'created_time', 'update', 'discount']
  inlines = [ProductCharacterInline, ProductImageInline,]
 
admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(Сharacteristic, ProductСharacteristicAdmin)
admin.site.register(Product, ProductAdmin)


class CategoryAdmin(MPTTModelAdmin):
    list_display = ['name', 'slug', 'image']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category, CategoryAdmin)