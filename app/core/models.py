from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)
class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('PhoneNumber is required')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)  # This handles password hashing
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
class User(AbstractBaseUser,PermissionsMixin):

    phone=models.CharField(max_length=15,primary_key=True)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)

    objects=UserManager()

    USERNAME_FIELD='phone'

class Customer(models.Model):
    user=models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    firstname=models.CharField(max_length=50)
    last_tname=models.CharField(max_length=50)
    email=models.EmailField(max_length=255,unique=True)

class Flower(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Order(models.Model):
   
    customer=models.ForeignKey(
        Customer,
        on_delete=models.CASCADE
    )
    created_at=models.DateTimeField(auto_now_add=True)

class orderItem(models.Model):
    flower=models.ForeignKey(
        Flower,
        on_delete=models.CASCADE
    )
    order=models.ForeignKey(
        Order,
        related_name="items",
        on_delete=models.CASCADE
    )
    quantity=models.PositiveIntegerField(default=1)
    price=models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.flower.name}"

