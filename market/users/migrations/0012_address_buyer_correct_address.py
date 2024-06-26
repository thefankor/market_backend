# Generated by Django 5.0.2 on 2024-03-22 15:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_buyer_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField()),
                ('region', models.CharField()),
                ('city', models.CharField()),
                ('index', models.CharField()),
                ('addr', models.CharField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='address', to='users.buyer')),
            ],
        ),
        migrations.AddField(
            model_name='buyer',
            name='correct_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='buyer', to='users.address'),
        ),
    ]
