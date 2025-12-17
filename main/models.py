from django.contrib.auth.models import AbstractUser, User
from django.db import models

class CorporateUser(AbstractUser):
    company_name = models.CharField(max_length=255)
    inn = models.CharField(max_length=12, unique=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)

    # username будет заменён на email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # что спрашивать при createsuperuser

    def __str__(self):
        return f"{self.company_name} ({self.email})"


class Order(models.Model):
    STATUS_CHOICES = [
        ('delivered', 'Доставлен'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('cancelled', 'Отменен'),
    ]

    user = models.ForeignKey(CorporateUser, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=20, unique=True)
    order_date = models.DateField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')
    description = models.TextField(blank=True)

    def __str__(self):
        return f"Заказ #{self.order_number}"
