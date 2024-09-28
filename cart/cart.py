from decimal import Decimal
from django.conf import settings
from shop.models.product_model import Product


class Cart:
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database.
        """
        product_uuids = self.cart.keys()  # Get the UUIDs from the cart
        products = Product.objects.filter(uuid__in=product_uuids)  # Query using UUIDs

        cart = self.cart.copy()
        for product in products:
            cart[str(product.uuid)]['product'] = product  # Use UUID as the key
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_uuid = str(product.uuid)  # Use UUID as the key
        if product_uuid not in self.cart:
            self.cart[product_uuid] = {
                'quantity': 0,
                'price': str(product.price)
            }
        if override_quantity:
            self.cart[product_uuid]['quantity'] = quantity
        else:
            self.cart[product_uuid]['quantity'] += quantity
        self.save()

    def save(self):
        """
        Mark the session as modified to ensure it gets saved.
        """
        self.session.modified = True

    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_uuid = str(product.uuid)
        if product_uuid in self.cart:
            del self.cart[product_uuid]
            self.save()

    def get_total_price(self):
        """
        Get the total price of items in the cart.
        """
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )

    def clear(self):
        """
        Remove the cart from the session.
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()
