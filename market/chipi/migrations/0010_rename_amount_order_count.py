# Generated by Django 5.0.2 on 2024-04-02 14:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chipi', '0009_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='amount',
            new_name='count',
        ),
    ]
