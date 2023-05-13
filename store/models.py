from django.db import models
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.validators import RegexValidator
import re
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from decimal import Decimal

import os
from uuid import uuid1
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Ссылка")
    image = models.ImageField(upload_to='category/', verbose_name="Изображение")

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name
    
class PodCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Под категория")
    name = models.CharField(max_length=255, verbose_name="Название", blank=True)
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Ссылка", blank=True)
    image = models.ImageField(upload_to='category/podcategory', verbose_name="Изображение", blank=True)

    class Meta:
        verbose_name = 'Под категория'
        verbose_name_plural = 'Под категории'

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    amount1 = models.IntegerField(verbose_name="Количество в шт", blank=True)
    amount2 = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Количество в граммах", blank=True)
    toorder = models.BooleanField(default=False, verbose_name="На заказ")
    stock = models.BooleanField(default=True, verbose_name="В наличии")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Ссылка", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    subcategory = models.ForeignKey(PodCategory, on_delete=models.CASCADE, verbose_name="Под категория")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    update = models.DateTimeField(auto_now=True, verbose_name="Время последнего обновления")
    discount = models.DecimalField(max_digits=4, decimal_places=2, default=0, verbose_name="Скидка")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = 'Товары'
    
    def save(self):
        super(Product, self).save()
        if not self.slug:
            self.slug = str(self.id)
            super(Product, self).save()
    
    def get_discounted_price(self):
        discounted_price = self.price - (self.price * self.discount / 100)
        return discounted_price
    
    def __str__(self):
        return self.name
    
class ProductImage(models.Model):
    def get_image_path(instance, filename):
        unique_id = str(instance.id) # id товара
        return os.path.join('product_images', unique_id, filename)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, related_name="images")
    image = models.ImageField(upload_to=get_image_path)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Изображение товара'
        verbose_name_plural = 'Изображения товаров'
    

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name="ФИО")
    email = models.EmailField(verbose_name="Почта")
    phone_regex = RegexValidator(
        regex=re.compile(r'^\+?1?\d{9,15}$'),
        message="Номер должен иметь формат: '+999999999'."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, verbose_name="Номер телефона")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.name

class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Имя клиента")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Название продукта")
    quantity = models.IntegerField(default=1, verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    address = models.CharField(max_length=255, verbose_name="Адрес доставки")
    date_ordered = models.DateTimeField(auto_now_add=True, verbose_name="Время заказа")
    is_completed = models.BooleanField(default=False, verbose_name="Готово?")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Ссылка", blank=True, null=True)
    
    def save(self):
        super(Order, self).save()
        if not self.slug:
            self.slug = str(self.id)
            super(Order, self).save()

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return self.Client.name

class Popular_product(models.Model):
    popular_product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Название продукта")
    start_date = models.DateTimeField(default=timezone.now, verbose_name="Начало времени показа")
    end_date = models.DateTimeField(null=True, blank=True, verbose_name="Конец времени показа")

    class Meta:
        verbose_name = 'Популярные товары'
        verbose_name_plural = 'Популярные товары'

    def __str__(self):
        return self.popular_product.name
    
class Newest_product(models.Model):
    new_product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Название продукта")
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
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Клиент")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Время создания")

    def __str__(self):
        return f"Cart {self.id} for {self.user.username}"

    def total(self):
        return sum(item.subtotal() for item in self.cart_items.all())
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='cart_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def subtotal(self):
        return self.quantity * Decimal(self.price)