from django.shortcuts import render, redirect, get_object_or_404
from store.models import *
from django.http import JsonResponse
import json
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def get_context(request):
    if request.user.is_authenticated:
        customer = request.user
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


def checkout(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    form = OrderRegister(request.POST or None, instance=order)

    if form.is_valid():
        order = form.save(commit=False)
        order.complete = True
        order.save()
        order_items = OrderItem.objects.filter(order=order)
        for order_item in order_items:
            order_item_obj = OrderItem.objects.filter(id=order_item.id)
            order_approve = OrderApprove.objects.create(customer=request.user, order=order, order_items_id=order_item.id )
            order_approve.save()

        messages.success(request, f'Order Successfully Placed! But yet to approve by Seller!')
        return redirect('store:home')

    items = order.orderitem_set.all()
    cart_items = order.get_cart_items
    products = Product.objects.all()
    context = {'products': products, 'cart_items': cart_items, 'order': order, 'items': items}
    form.fields['shipping_address'].queryset = CustomerAddress.objects.filter(customer_id=request.user.id)
    context['form'] = form
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


def add_address(request):
    context = get_context(request)
    if request.method == "POST":
        form = CustomerAddressRegister(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Address created!')
            return redirect('store:checkout', order_id=context['order'].id)

    form = CustomerAddressRegister()
    form.fields['customer'].queryset = Account.objects.filter(id=request.user.id)
    context['form'] = form
    return render(request, 'store/address.html', context)


def orders(request):
    context = get_context(request)
    orders_set = Order.objects.filter(customer=request.user)
    order_with_details = []
    i = 0
    for order_id in orders_set:
        order_items = OrderItem.objects.filter(order_id=order_id.id)
        for order_item in order_items:
            product = Product.objects.filter(id=order_item.product_id)[0]
            order_approve = OrderApprove.objects.filter(order_items_id=order_item.id)[0]
            seller = Account.objects.filter(id=product.seller_id)[0]
            entry = {'order_id': order_id.id, 'product_name': product.name, 'quantity': order_item.quantity,
                     'price': product.price, 'status': order_approve.approve_status, 'seller_name': seller.first_name,
                     'seller_id': seller.id}
            order_with_details.append(entry)

    context['order_with_details'] = order_with_details
    return render(request, 'store/orders.html', context)


@login_required
def orders_status(request, order_approve_item_id=None):
    orders_to_approve = []
    products = Product.objects.filter(seller=request.user)
    for product in products:
        ordered_items = OrderItem.objects.filter(product_id=product.id)
        for order_item in ordered_items:
            orders_approve_pending = OrderApprove.objects.filter(order_items_id=order_item.id,
                                                                 approve_status="On Pending")
            if orders_approve_pending:
                orders_approve_pending = orders_approve_pending[0]
                order_details = {'order_id': orders_approve_pending.order.id, 'product_name': product.name,
                                 'price': product.price, 'quantity': order_item.quantity,
                                 'status': orders_approve_pending.approve_status,
                                 'customer': orders_approve_pending.customer.email,
                                 'approve_id': orders_approve_pending.id}
                orders_to_approve.append(order_details)
                print(order_details)

    return render(request, 'store/orders_status.html', {'orders': orders_to_approve})


def update_status(request):
    data = json.loads(request.body)
    approve_id = data['approve_status']
    action = data['action']

    order_approve = OrderApprove.objects.get(id=approve_id)
    print(order_approve)

    if action == 'approve':
        order_approve.approve_status = "Approved"

    elif action == 'reject':
        order_approve.approve_status = "Rejected"

    order_approve.save()

    return JsonResponse('Item was added', safe=False)




@login_required
def orders_approved(request):
    pass