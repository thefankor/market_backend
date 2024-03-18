from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    is_buyer = models.BooleanField(default=False)
    is_shop = models.BooleanField(default=False)


class Buyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, related_name='buyer')
    first_name = models.CharField(max_length=63, blank=True)
    middle_name = models.CharField(max_length=63, blank=True)
    last_name = models.CharField(max_length=63, blank=True)
    email = models.EmailField(blank=True, unique=True, null=True)
    phone = models.CharField(blank=True, null=True, unique=True)
    sex = models.BooleanField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.user.username

