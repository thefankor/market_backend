from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import Product, Review, Category, Shop, Cart, ProdCategory
# Register your models here.


class CategoryAdmin(MPTTModelAdmin):
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(ProdCategory, CategoryAdmin)



admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Shop)
admin.site.register(Review)
admin.site.register(Cart)


