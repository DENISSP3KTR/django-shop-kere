# Generated by Django 4.2 on 2023-05-04 14:02

from django.db import migrations, models
import store.models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_cart_alter_productimage_product_cartitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(upload_to=store.models.ProductImage.get_image_path),
        ),
    ]
