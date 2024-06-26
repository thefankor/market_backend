# Generated by Django 5.0.2 on 2024-03-11 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_buyer_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyer',
            name='email',
            field=models.EmailField(blank=True, max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='buyer',
            name='phone',
            field=models.BigIntegerField(blank=True, null=True, unique=True),
        ),
    ]
