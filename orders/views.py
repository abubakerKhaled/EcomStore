from django.shortcuts import render
from cart.cart import Cart
from .forms import OrderCreateForm
from .models import OrderItem


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order = order,
                    product = item['product'],
                    price = item['price'],
                    quantity = item['quantity']
                )
            # clear the cart
            cart.clear()
            context = {
                'order': order
            }
            return render(
                request, 'orders/order/created.html', context
            )
    else:
        form = OrderCreateForm()
        context = {
            'cart': cart,
            'form': form
        }
        return render(
            request, 
            'orders/order/create.html',
            context 
        )
