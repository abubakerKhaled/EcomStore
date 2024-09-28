from django import forms
from .models import OrderItem
from .models import Order

class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = '__all__'

    # Override the price field widget
    price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.TextInput(attrs={'type': 'text'})
    )

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
        'first_name',
        'last_name',
        'email',
        'address',
        'postal_code',
        'city',
        ]