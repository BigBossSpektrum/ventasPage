# Generated by Django 5.1.3 on 2024-12-17 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_rename_img_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='static/products/img'),
        ),
    ]