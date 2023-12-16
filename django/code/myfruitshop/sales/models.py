from django.db import models
from django.contrib.auth.models import User

class Fruit(models.Model):
    name = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Sale(models.Model):
    fruit = models.ForeignKey(Fruit, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_amount = models.PositiveIntegerField()
    sale_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.fruit.name} - {self.quantity} units - {self.sale_date}"
