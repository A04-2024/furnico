# Generated by Django 5.1.1 on 2024-10-23 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('show_products', '0012_alter_categories_unique_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='categories',
            name='image_url',
            field=models.CharField(default=0, max_length=10000),
            preserve_default=False,
        ),
    ]
