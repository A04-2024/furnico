import os
import csv
from django.core.management import execute_from_command_line
from django.conf import settings

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'furnico.settings')

# Initialize Django
import django
django.setup()

from show_products.models import *

def run():
    categories = [
        Categories.objects.create(category_name="Kursi", image_url="https://d2xjmi1k71iy2m.cloudfront.net/dairyfarm/id/pageImages/page__en_us_1726029609182_4_6.webp"),
        Categories.objects.create(category_name="Meja", image_url="https://d2xjmi1k71iy2m.cloudfront.net/dairyfarm/id/pageImages/page__en_us_1720414006605_3_13.webp"),
        Categories.objects.create(category_name="Bangku", image_url="https://d2xjmi1k71iy2m.cloudfront.net/dairyfarm/id/pageImages/page__en_us_1726029608858_4_3.webp"),
        Categories.objects.create(category_name="Sofa", image_url="https://d2xjmi1k71iy2m.cloudfront.net/dairyfarm/id/pageImages/page__en_us_1726029608940_4_4.webp"),
        Categories.objects.create(category_name="Dekorasi", image_url="https://d2xjmi1k71iy2m.cloudfront.net/dairyfarm/id/pageImages/page__en_us_1726029609339_4_7.webp"),
    ]

    with open("dataset.csv", encoding='latin') as f:
        # Change the delimiter to ';'
        reader = csv.reader(f, delimiter=';')
        next(reader)
        i = 0
        for row in reader:
            product_image = row[0]
            product_name = row[1]
            product_subtitle = row[2]
            product_price = row[3]
            sold_this_week = row[4]
            people_bought = row[5]
            product_description = row[6]
            product_advantages = row[7]
            product_material = row[8]
            product_size_length = row[9]
            product_size_height = row[10]
            product_size_long = row[11]

            Product.objects.create(
                product_image=product_image,
                product_name=product_name,
                product_subtitle=product_subtitle,
                product_price=product_price,
                sold_this_week=sold_this_week,
                people_bought=people_bought,
                product_description=product_description,
                product_advantages=product_advantages,
                product_material=product_material,
                product_size_length=product_size_length,
                product_size_height=product_size_height,
                product_size_long=product_size_long,
                product_category=categories[i % 5],
                product_rating=0
            )
            i += 1

if __name__ == "__main__":
    run()
