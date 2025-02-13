from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomerManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        # normalize_email makes email addresses lowercase
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # This handles password hashing
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # Superusers should have admin privileges
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
# Create your models here.
class Flower(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Customer(AbstractBaseUser):
    fname=models.CharField(max_length=100)
    lname=models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
     
    objects = CustomerManager()  # This line is missing - it connects your manager
    USERNAME_FIELD = 'email'

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

