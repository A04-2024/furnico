# Generated by Django 5.1.1 on 2024-10-24 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(choices=[('info_error', 'Kesalahan info furniture'), ('image_error', 'Gambar furniture salah atau kurang jelas'), ('website_issue', 'Masalah pada website'), ('pricing_error', 'Kesalahan harga'), ('out_of_stock', 'Barang tidak tersedia'), ('slow_performance', 'Website lambat atau tidak responsif'), ('layout_issue', 'Tampilan website tidak rapi'), ('other', 'Lainnya')], max_length=50)),
                ('additional_info', models.TextField(blank=True, null=True)),
                ('date_reported', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
