from django.shortcuts import render, redirect, get_object_or_404
from store.models import *
from django.http import JsonResponse
import json
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import string, random


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


@login_required
def cart(request):
    context = get_context(request)
    return render(request, 'store/cart.html', context)


@login_required
def checkout(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    form = OrderRegister(request.POST or None, instance=order)

    if form.is_valid():
        order = form.save(commit=False)
        order.complete = True
        order.save()
        trxn_id = str(order_id) + ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))
        order_items = OrderItem.objects.filter(order=order)
        for order_item in order_items:
            order_approve = OrderApprove.objects.create(customer=request.user,
                                                        order=order,
                                                        order_items_id=order_item.id,
                                                        seller=order_item.product.seller,
                                                        product_name=order_item.product.name,
                                                        price=order_item.product.price,
                                                        total=order.get_cart_items,
                                                        quantity=order_item.quantity,
                                                        approve_status="On Pending",
                                                        transaction_id=trxn_id,
                                                        seller_name=order_item.product.seller.first_name
                                                        )
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


@login_required
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


@login_required
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


@login_required
def orders(request):
    context = get_context(request)
    orders_set = OrderApprove.objects.filter(customer=request.user)
    context['order_with_details'] = orders_set
    return render(request, 'store/orders.html', context)


def get_orders(request, is_order_history):
    if is_order_history:
        return OrderApprove.objects.filter(seller=request.user).exclude(approve_status="On Pending")
    return OrderApprove.objects.filter(seller=request.user, approve_status="On Pending")


@login_required
def orders_status(request):
    orders_to_approve = get_orders(request, False)
    return render(request, 'store/orders_status.html', {'orders': orders_to_approve})


@login_required
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
def orders_history(request):
    order_list = get_orders(request, True)
    return render(request, 'store/orders_status.html', {'orders': order_list})


@login_required
def product_create(request):
    if request.method == "POST":
        form = ProductRegister(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            img = form.cleaned_data.get("image")
            desc = form.cleaned_data.get("description")
            seller = form.cleaned_data.get("seller")
            price = form.cleaned_data.get("price")
            category = form.cleaned_data.get("category")
            new_product = Product.objects.create(name=name,
                                                 image=img,
                                                 description=desc,
                                                 seller=seller,
                                                 price=price,
                                                 category=category)
            new_product.save()
            messages.success(request, f'Product added!')
            return redirect('store:home')

    form = ProductRegister()
    form.fields['seller'].queryset = Account.objects.filter(id=request.user.id)
    return render(request, 'store/product_register.html', {'form': form})


@login_required
def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    form = ProductRegister(request.POST or None, instance=product)

    if form.is_valid():
        product = form.save(commit=False)
        product.name = form.cleaned_data.get("name")
        product.image = form.cleaned_data.get("image")
        product.description = form.cleaned_data.get("description")
        product.seller = form.cleaned_data.get("seller")
        product.price = form.cleaned_data.get("price")
        product.category = form.cleaned_data.get("category")
        product.save()
        messages.success(request, f'Product details updated!')
        return redirect('store:home')

    return render(request, 'store/update_product.html', {'form': form})


@login_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()

    return redirect('store:home')


@login_required
def add_category(request):
    if request.method == "POST":
        form = CategoryRegister(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.category = form.cleaned_data.get('category')
            category.save()
            return redirect('store:home')
        else:
            messages.warning(request, f'Category already present!')

    form = CategoryRegister()
    category_list = Category.objects.all()
    return render(request, 'store/add_category.html', {'form': form, 'categories': category_list})


@login_required
def update_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    form = CategoryRegister(request.POST or None, instance=category)
    if form.is_valid():
        category.category = form.cleaned_data.get('category')
        category.save()
        return redirect('store:home')

    return render(request, 'store/update_category.html', {'form': form})