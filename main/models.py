from django.contrib.auth.models import User
from django.db import models



class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)
    avatar = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    in_stock = models.BooleanField(default=True)
    quantity = models.PositiveIntegerField(default=0)

    image_url = models.URLField(blank=True)  # главное изображение
    slug = models.SlugField(unique=True)

    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.URLField()
    alt = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.product.title}"


class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")

    author = models.CharField(max_length=255)
    rating = models.PositiveIntegerField(default=5)
    text = models.TextField()
    created_at = models.DateField()

    def __str__(self):
        return f"{self.author} — {self.rating}★"

class OrderStatus(models.TextChoices):
    NEW = "new", "Новый"
    PROCESSING = "processing", "В обработке"
    PRODUCTION = "production", "В производстве"
    READY = "ready", "Готов к выдаче"
    DELIVERED = "delivered", "Доставлен"
    CANCELED = "canceled", "Отменён"


STATUS_COLOR = {
    "new": "secondary",
    "processing": "warning",
    "production": "info",
    "ready": "primary",
    "delivered": "success",
    "canceled": "danger",
}


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="orders")

    number = models.PositiveIntegerField(unique=True)
    created_at = models.DateField()
    expected_date = models.DateField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.NEW
    )

    action_label = models.CharField(max_length=255, blank=True)

    @property
    def status_label(self):
        """Строковое отображение статуса."""
        return OrderStatus(self.status).label

    @property
    def status_color(self):
        return STATUS_COLOR.get(self.status, "secondary")

    @property
    def amount(self):
        total = sum(item.total_price for item in self.items.all())
        return total

    def __str__(self):
        return f"Заказ #{self.number}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)

    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product} x {self.quantity}"
