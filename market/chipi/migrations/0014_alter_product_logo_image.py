# Generated by Django 5.0.2 on 2024-04-04 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chipi', '0013_product_logo_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='logo_image',
            field=models.ImageField(upload_to='logos/'),
        ),
    ]
