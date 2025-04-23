import random
import string

from django.shortcuts import render

from .utils import get_or_create_cart, init
from accounts.models import User


# Create your views here.

def checkout_view(request):
    init()
    total_price = 0
    if request.method == 'POST':
        items = request.POST.get('user_input').upper().strip().split('\n')
        items_count = len(items[0])

        #create cart
        map = {}
        #dummy user for usage
        user = User(username=''.join(random.choice(string.ascii_letters) for x in range(4)))
        user.save()

        cart = get_or_create_cart(user )

        #add cart items to the cart  for persistence across sessions
        # not being used currently
        for i in range(items_count):
            item = items[0][i]
            cart.add_item(item)


        #caluclate total
        total_price = cart.calculate_total()

    return render(request, "form.html", {"output": total_price})



