from django.db import transaction

from .model.cart import Cart
from .model.priceSlab import PriceSlab
from agrichain.model.product import Product


def get_or_create_cart(userOb,cart_id="123"):
    if cart_id:
        try:
            return Cart.objects.get(pk=cart_id)
        except Cart.DoesNotExist:
            pass
    cart = Cart.objects.create( user=userOb)
    return cart




def init():
    #DELETE OLD


    try:
        with transaction.atomic():
            PriceSlab.objects.all().delete()
            Product.objects.all().delete()
    except Exception as e:
        print(f"Error deleting products: {e}")

    # initalize product and price slabs
    product_a = Product.objects.create(name='A')
    product_b = Product.objects.create(name='B')
    product_c = Product.objects.create(name='C')
    product_d = Product.objects.create(name='D')

    #addding price slabs
    PriceSlab.objects.create( product=product_a, qty=1 , price=50 )
    PriceSlab.objects.create( product=product_a, qty=2 , price=80 )

    PriceSlab.objects.create( product=product_b, qty=1 , price=30 )
    PriceSlab.objects.create( product=product_b, qty=2 , price=50 )

    PriceSlab.objects.create( product=product_c, qty=1 , price=40 )

    PriceSlab.objects.create( product=product_d, qty=1 , price=20 )











