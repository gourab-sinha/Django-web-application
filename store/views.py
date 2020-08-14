from django.shortcuts import render
from store.models import *


def home(request):
    if request.user.is_authenticated:
        if request.user.account_type == "MANAGER":
            products = Product.objects.filter(seller=request.user.id)
            return render(request, 'store/store.html', {'products': products})

    products = Product.objects.all()
    return render(request, 'store/store.html', {'products': products})


def cart(request):
    context = {}
    return render(request, 'store/cart.html', context)


def checkout(request):
    context = {}
    return render(request, 'store/checkout.html', context)


def add_product(request):
    pass


def update_product(request):
    pass


def delete_product(request):
    pass


def add_to_cart(request):
    pass


def place_order(request):
    pass





