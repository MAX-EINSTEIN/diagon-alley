import json
from django.shortcuts import render
from .models import *
from django.http import JsonResponse

# Create your views here.\


def home(request):
    return render(request, 'store/home.html', {})


def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, _ = Order.objects.get_or_create(
            customer=customer, state='Ordered')
        items = order.orderitem_set.all()
        cartItems = order.get_total_quantity
    else:
        items = []
        order = {'get_total_price': 0, 'get_total_quantity': 0}
        cartItems = order['get_total_quantity']
    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, _ = Order.objects.get_or_create(
            customer=customer, state='Ordered')
        items = order.orderitem_set.all()
        cartItems = order.get_total_quantity
    else:
        items = []
        order = {'get_total_price': 0, 'get_total_quantity': 0}
        cartItems = order['get_total_quantity']
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, _ = Order.objects.get_or_create(
            customer=customer, state='Ordered')
        items = order.orderitem_set.all()
        cartItems = order.get_total_quantity
    else:
        items = []
        order = {'get_total_price': 0, 'get_total_quantity': 0}
        cartItems = order['get_total_quantity']
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print(productId, action)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, _ = Order.objects.get_or_create(
        customer=customer, state='Ordered')
    orderItem, _ = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)
