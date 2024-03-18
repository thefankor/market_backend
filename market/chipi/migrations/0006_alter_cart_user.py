# Generated by Django 5.0.2 on 2024-03-17 15:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chipi', '0005_cart'),
        ('users', '0011_alter_buyer_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart', to='users.buyer'),
        ),
    ]
