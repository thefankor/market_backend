from django.contrib import admin

from .models import Product, Review, Category, Shop, Cart
# Register your models here.

admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Shop)
admin.site.register(Review)
admin.site.register(Cart)


