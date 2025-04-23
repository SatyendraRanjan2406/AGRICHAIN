from django import forms


# form for adding an item to the cart
class CheckoutForm(forms.Form):
    items = forms.CharField(max_length=255 , required=True)




