from django.db import models
from django.urls import reverse
from users.models import User, Buyer


# from users.models import User
# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.IntegerField()
    count = models.IntegerField(default=0)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='products')
    shop = models.ForeignKey('Shop', on_delete=models.PROTECT, related_name='products')
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse('product', kwargs={'product_id': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["pk"]


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name



class Shop(models.Model):
    '''- id
        - seller_id
        - name
        - (Rating)
        - (Sklad address)'''
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, related_name='shop', null=True)
    name = models.CharField(max_length=63, db_index=True)
    email = models.EmailField(blank=True, unique=True, null=True)
    phone = models.BigIntegerField(blank=True, unique=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop', kwargs={'seller_id': self.pk})

    class Meta:
        ordering = ["pk"]


class Review(models.Model):
    '''
    FEEDBACKS
    - Id
    - Text
    - user_id
    - product_id
    - Created
    - Rate
    '''
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='reviews')
    from_user = models.IntegerField(null=True, blank=True)
    text = models.TextField(blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    score = models.IntegerField()


class Cart(models.Model):
    user = models.ForeignKey(Buyer, on_delete=models.CASCADE, related_name='cart')
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='cart')
    count = models.PositiveIntegerField(default=1)
    time_created = models.DateTimeField(auto_now_add=True)
    time_updated = models.DateTimeField(auto_now=True)

    def sum(self):
        return self.count * self.product.price
