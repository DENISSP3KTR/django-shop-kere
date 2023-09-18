from django.db import models
from django.contrib.auth.models import AbstractUser
from mptt.models import MPTTModel, TreeForeignKey
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.validators import RegexValidator
import re
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from decimal import Decimal
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.urls import reverse
import os
from uuid import uuid1

class Category(MPTTModel):
    name = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Ссылка")
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='Подкатегория')
    image = models.ImageField(upload_to='category/', verbose_name="Изображение")
    
    class MPTTMeta:
        order_insertion_by = ['name']
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def save(self, *args, **kwargs):
        super(Category, self).save(*args, **kwargs)
        Category.objects.rebuild()

    def get_absolute_url(self):
        return reverse('store:category_view', args=[self.slug])
    
    def __str__(self):
        return self.name
    
    
class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название", unique=False)
    description = models.TextField(verbose_name="Описание", unique=False, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    amount1 = models.IntegerField(verbose_name="Количество в шт", null=True, blank=True)
    toorder = models.BooleanField(default=False, verbose_name="На заказ")
    stock = models.BooleanField(default=True, verbose_name="В наличии")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Ссылка", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория", related_name="products")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    update = models.DateTimeField(auto_now=True, verbose_name="Время последнего обновления")
    discount = models.DecimalField(max_digits=4, decimal_places=2, default=0, verbose_name="Скидка")
    
    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = 'Товары'
    
    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.slug])
    
    def __str__(self):
        return self.name
    
class Сharacteristic(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, related_name="product_character")
    characteristic = models.CharField(max_length=255, verbose_name="Характеристика товара", unique=False)
    class Meta:
        verbose_name = 'Характеристика товара'
        verbose_name_plural = 'Характеристики товара'

    def __str__(self):
        return self.product.name
    
class ProductImage(models.Model):
    def get_image_path(instance, filename):
        unique_id = str(instance.id) # id товара
        return os.path.join('product_images', unique_id, filename)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, related_name="product_images")
    image = models.ImageField(upload_to=get_image_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товаров'
    
    def __str__(self):
        return self.product.name
    
@receiver(post_save, sender=Product)
def generate_slug(sender, instance, created, **kwargs):
    if created and not instance.slug:
        instance.slug = slugify(f"{instance.id}-{instance.name}")
        instance.save()


class Client(AbstractUser):
    patronymic = models.CharField(max_length=50, verbose_name="Отчество")
    phone_regex = RegexValidator(
        regex=re.compile(r'^\+?1?\d{9,15}$'),
        message="Номер должен иметь формат: '+999999999'."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, verbose_name="Номер телефона")
    sogl = models.BooleanField(default=False)
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Ссылка", blank=True, null=True)
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.email
@receiver(post_save, sender=Client)
def generate_slug(sender, instance, created, **kwargs):
    if created and not instance.slug:
        instance.slug = slugify(f"{instance.id}")
        instance.save()
class OrderStatus(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Имя клиента")
    product = models.ManyToManyField(Product, through='OrderItem')
    delivery_parametr = models.BooleanField(default=False, verbose_name="Самовывоз")
    address = models.CharField(max_length=255, verbose_name="Адрес доставки", blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True, verbose_name="Время заказа")
    is_completed = models.BooleanField(default=False, verbose_name="Готово?")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Ссылка", blank=True, null=True)
    status = models.ForeignKey(OrderStatus, on_delete=models.SET_NULL, null=True, verbose_name="Статус заказа")
    def save(self):
        super(Order, self).save()
        if not self.slug:
            self.slug = str(self.id)
            super(Order, self).save()

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"{self.client} - Заказ {self.pk}"
    
@receiver(post_save, sender=Order)
def generate_slug(sender, instance, created, **kwargs):
    if created and not instance.slug:
        instance.slug = slugify(f"{instance.id}")
        instance.save()
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Название продукта")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    def __str__(self):
        return f"{self.order} - {self.product}"
    
    def subtotal(self):
        return self.quantity * Decimal(self.product.price)
    
class Popular_product(models.Model):
    popular_product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Название продукта", related_name="popular_product")
    start_date = models.DateTimeField(default=timezone.now, verbose_name="Начало времени показа")
    end_date = models.DateTimeField(null=True, blank=True, verbose_name="Конец времени показа")

    class Meta:
        verbose_name = 'Популярные товары'
        verbose_name_plural = 'Популярные товары'

    def __str__(self):
        return self.popular_product.name
    
class Newest_product(models.Model):
    new_product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Название продукта", related_name="new_product")
    start_date = models.DateTimeField(default=timezone.now, verbose_name="Начало времени показа")
    end_date = models.DateTimeField(null=True, blank=True, verbose_name="Конец времени показа")

    class Meta:
        verbose_name = 'Новые товары'
        verbose_name_plural = 'Новые товары'

    def __str__(self):
        return self.new_product.name
    
class Sale_product(models.Model):
    sale_product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Название продукта")

    class Meta:
        verbose_name = 'Распродажа'
        verbose_name_plural = 'Распродажа'

    def __str__(self):
        return self.sale_product.name
