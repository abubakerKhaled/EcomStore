from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, render, redirect
from cart.cart import Cart
from .forms import OrderCreateForm
from .models import OrderItem, Order
from .tasks import order_created
import weasyprint
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.conf import settings



def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order = order,
                    product = item['product'],
                    price = item['price'],
                    quantity = item['quantity']
                )
            # clear the cart
            cart.clear()
            # Launch asynchronous task
            order_created.delay(order.id)

            # set the order in the session
            request.session['order_id'] = order.id
            # redirect for payment
            return redirect('payment:process')
        
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
    



## View to generate the pdf
@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order_id}.pdf'
    weasyprint.HTML(string=html).write_pdf(
        response,
        stylesheets=[weasyprint.CSS(settings.BASE_DIR / 'static/css/pdf.css')]

    )
    return response




@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {
        'order': order
    }
    return render(
        request, 'admin/orders/order/detail.html', context
    )