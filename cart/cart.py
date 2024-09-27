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

    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        ## Get the product id 
        ## JSON uses string keys only
        product_id = str(product.id)
        ## If the product id not in the cart
        if product_id not in self.cart:
            ## Initialize the new cart item
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }
        ## If we want to override the quantity
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        ## Else we add quantity to the old quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        # make the session as 'modified' to make sure it gets saved
        self.session.modified = True

    def remove(self, product):
        """
        Remove the product form the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()