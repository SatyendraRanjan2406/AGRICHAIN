from django.db import models

from .priceSlab import PriceSlab
from .product import Product
from ..exception import ItemNotFoundException, CartItemException, CartException
from accounts.models import User


class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    checkout_at = models.DateTimeField(null=True, blank=True)


    """ 
    Add items to cart or incerement its qty  if exist already.
    Args: product name
    Returns : True if sucessful else False
    Raises : ItemNotFoundException : if product not found
             CartItemException : if cart item not saved
    """

    def add_item(self , name):
        from .cartItem import CartItem

        # add item to cart
        try:
            product = Product.objects.get(name=name)
        except Product.DoesNotExist:
            raise ItemNotFoundException(f"product {name} not found")

        #save to cart item
        try:
            cart_item,created = CartItem.objects.get_or_create( product=product,cart=self )
            cart_item.qty += 1
            cart_item.save()
            return True
        except Exception as e:
            raise CartItemException(f"failed to save cartitem : {str(e)}")



    """ 
    Remove items from cart if qty is 0 or decremnt its qty  if  >1
    Args: product name
    Returns : True if sucessful else False
    Raises : ItemNotFoundException : if product not found
             CartItemException : if cart item not removed
    """

    def remove_item(self,  name):
        from .cartItem import CartItem

        # decrement item quantity or remove item from cart if qty==0
        try:
            product = Product.objects.get(name=name)
        except Product.DoesNotExist:
            raise ItemNotFoundException(f"product {name} not found")

        #remove item or decrement qty
        try:
            cart_item = CartItem.objects.get(product=product)
            cart_item.qty -=1
            if cart_item.quantity == 0:
                cart_item.delete()
        except CartItem.DoesNotExist:
            raise CartItemException(f"cart item for '{product.name}' not found")
        except Exception as e:
            raise CartItemException(f"failed to remove cartitem : {str(e)}")
        return None


    """
    Calculate total price of cart based on price slabs 
    Returns : float 
    Raises : CartException : if cart total cannot be calculated
    """


    def calculate_total(self):
        total = 0
        try:
            cart_items = self.cart_items.all()
            for item in cart_items:
                slabs = PriceSlab.objects.all().filter(product=item.product).order_by('-qty')

                # qty in cart of cart item
                remaining_qty = item.qty
                for slab in slabs:
                    multiplier = remaining_qty//slab.qty
                    total += multiplier * slab.price
                    remaining_qty -= multiplier * slab.qty

            return total
        except Exception as e:
            raise CartException(f"failed to calculate total cartitem : {str(e)}")


    """
    Removes all cart Items
    Returns : True if sucessful else False
    """
    def clearCart(self):
        try:
            self.cart_items.all().delete()
            return True
        except Exception as e:
            return False


