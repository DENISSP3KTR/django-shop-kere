from django.contrib import admin

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
  list_display = ['name', 'description', 'price', 'amount1', 'amount2', 'stock', 'category', 'subcategory', 'created_time', 'update', 'discount']
  prepopulated_fields = {'slug': ('name',)}
  inlines = [ProductImageInline,]
  list_filter = ('category', 'subcategory')
  def formfield_for_foreignkey(self, db_field, request, **kwargs):
    if db_field.name == 'subcategory':
        # Получаем выбранную категорию
        category_id = request.POST.get('category')
        if category_id:
            # Фильтруем подкатегории по выбранной категории
            kwargs['queryset'] = PodCategory.objects.filter(category_id=category_id)
        else:
            # Если категория не выбрана, показываем все подкатегории
            kwargs['queryset'] = PodCategory.objects.all()
    return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(ProductImage, ProductImageAdmin)
admin.site.register(Product, ProductAdmin)

class PodCategoryAdmin(admin.ModelAdmin):
   pass

class PodCategoryInline(admin.TabularInline):
   prepopulated_fields = {'slug': ('name',)}
   model = PodCategory
   max_num = 10
   extra = 0

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'image']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    inlines = [PodCategoryInline,]

admin.site.register(PodCategory, PodCategoryAdmin)
admin.site.register(Category, CategoryAdmin)