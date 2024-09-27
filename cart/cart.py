from decimal import Decimal
from django.conf import settings
from shop.models.product_model import Product


class Cart:
    def __init__(self, request):
        """
        Initialize the cart.
        """
        ## Store the session from the request object
        self.session = request.session
        ## Get the cart from the session
        cart = self.session.get(settings.CART_SESSION_ID)
        ## If the cart empty or not setup
        if not cart:
            # Save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        ## Store the new cart into the cart variable
        self.cart = cart
