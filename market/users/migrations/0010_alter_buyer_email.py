# Generated by Django 5.0.2 on 2024-03-11 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_buyer_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyer',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
    ]
