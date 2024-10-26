# Generated by Django 4.2.11 on 2024-10-24 15:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('show_products', '0013_categories_image_url'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rating', '0006_alter_productrating_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='productrating',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='show_products.product'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productrating',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]