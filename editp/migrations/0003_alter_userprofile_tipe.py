# Generated by Django 5.1.1 on 2024-10-25 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('editp', '0002_userprofile_tipe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='tipe',
            field=models.CharField(blank=True, choices=[('user', 'User'), ('admin', 'Admin')], max_length=10, null=True),
        ),
    ]
