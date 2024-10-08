from celery import shared_task
from django.core.mail import send_mail
from .models import Order


@shared_task
def order_created(order_id):
    """
    Task to sned an email notification when an order is 
    successfully created.
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = (
        f'Dear {order.first_name}, \n\n'
        f'You have successfully placed an order.\n'
        f'Your order ID is {order.id}.\n'
    )
    main_sent = send_mail(
        subject, message, 'admin@ecomstore.com', [order.email]
        )
    return main_sent

