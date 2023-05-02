from django.db import models
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.validators import RegexValidator
import re
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Ссылка")
    image = models.ImageField(upload_to='img/', verbose_name="Изображение")

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    price = models.DecimalField(max_digits=4, decimal_places=2, verbose_name="Цена")
    image = models.ImageField(upload_to='img/', verbose_name="Изображение")
    amount = models.IntegerField(verbose_name="Количество")
    stock = models.BooleanField(default=True, verbose_name="Наличие")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Ссылка", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    update = models.DateTimeField(auto_now=True, verbose_name="Время последнего обновления")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = 'Товары'
    
    def save(self):
        super(Product, self).save()
        if not self.slug:
            self.slug = str(self.id)
            super(Product, self).save()

    def __str__(self):
        return self.name

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
        return self.popular_product.name