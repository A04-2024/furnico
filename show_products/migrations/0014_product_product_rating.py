# Generated by Django 5.1.1 on 2024-10-26 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('show_products', '0013_categories_image_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_rating',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=False,
        ),
    ]
