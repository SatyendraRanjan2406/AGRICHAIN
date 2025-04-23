from django.db import models
from .cart import Cart
from .product import Product


class CartItem(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=0)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    item_added = models.DateTimeField(auto_now_add=True)
    item_updated = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ('product', 'cart')




