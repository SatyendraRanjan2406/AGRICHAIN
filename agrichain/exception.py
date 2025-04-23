

class ItemNotFoundException(Exception):
    # when item is not found in the cart
    pass


class CartException(Exception):
    # Base exception class for Cart Related errors
    pass

class CartItemException(Exception):
    pass


