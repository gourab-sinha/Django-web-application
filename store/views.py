from django.shortcuts import render
from store.models import *
from django.http import JsonResponse
import json


def get_context(request):
    if request.user.is_authenticated:
        customer = request.user.id
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
        products = Product.objects.all()
        context = {'products': products, 'cart_items': cart_items, 'order': order, 'items': items}
        return context

    products = Product.objects.all()
    items = []
    order = {'get_cart_items': 0, 'get_cart_total': 0}
    cart_items = order['get_cart_items']
    context = {'products': products, 'cart_items': cart_items, 'order': order, 'items': items }
    return context


def home(request):
    if request.user.is_authenticated:
        if request.user.account_type == "MANAGER":
            products = Product.objects.filter(seller=request.user.id)
            return render(request, 'store/store.html', {'products': products})

    context = get_context(request)
    return render(request, 'store/store.html', context)


def cart(request):
    context = get_context(request)
    return render(request, 'store/cart.html', context)


def checkout(request):
    context = get_context(request)
    return render(request, 'store/checkout.html', context)


def update_item(request):
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']

    customer = request.user.id
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        order_item.quantity = (order_item.quantity +1)
    elif action == 'remove':
        order_item.quantity = (order_item.quantity - 1)

    order_item.save()
    if order_item.quantity <= 0:
        order_item.delete()

    return JsonResponse('Item was added', safe=False)