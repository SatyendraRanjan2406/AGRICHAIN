from django.db import models
from .product import Product


class PriceSlab(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='price_slabs')
    qty = models.PositiveIntegerField()
    price = models.PositiveIntegerField()

