# Generated by Django 5.0.2 on 2024-04-02 19:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chipi', '0010_rename_amount_order_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shop',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='chipi.shop'),
        ),
    ]