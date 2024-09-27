from django.shortcuts import render, get_object_or_404
from ..models.product_model import Product
from ..models.category_model import Category
from cart.forms import CartAddProductForm

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)
    context = {
        'category': category,
        'categories': categories,
        'products': products
    }
    return render(
        request,
        'shop/product/list.html',
        context)


def product_detail(request, uuid, slug):
    product = get_object_or_404(
        Product, uuid=uuid, slug=slug, available=True
    )
    cart_product_form = CartAddProductForm()
    context = {
        'product': product,
        'cart_product_form': cart_product_form,
        }
    return render(
        request,
        'shop/product/details.html',
        context)