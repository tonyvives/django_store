from django.shortcuts import render, redirect
from .models import Cart, CartItem, Order, OrderItem
from products.models import Product
from django.core.exceptions import ObjectDoesNotExist
import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)

    cart, created = Cart.objects.get_or_create(cart_id=_cart_id(request))

    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
        cart_item.save()

    return redirect("cart_detail")


def cart_detail(request, cart_items=None):
    total = 0
    counter = 0
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total += cart_item.product.price * cart_item.quantity
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass

    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_total = int(total * 100)
    description = "Django Store - New Order"
    data_key = settings.STRIPE_PUBLISHABLE_KEY

    if request.method == "POST":
        try:
            token = request.POST["stripeToken"]
            email = request.POST["stripeEmail"]
            billingName = request.POST["stripeBillingName"]
            billingAddress1 = request.POST["stripeBillingAddressLine1"]
            billingCity = request.POST["stripeBillingAddressCity"]
            billingPostcode = request.POST["stripeBillingAddressZip"]
            billingCountry = request.POST["stripeBillingAddressCountryCode"]
            shippingName = request.POST["stripeShippingName"]
            shippingAddress1 = request.POST["stripeShippingAddressLine1"]
            shippingCity = request.POST["stripeShippingAddressCity"]
            shippingPostcode = request.POST["stripeShippingAddressZip"]
            shippingCountry = request.POST["stripeShippingAddressCountryCode"]
            customer = stripe.Customer.create(email=email, source=token)
            charge = stripe.Charge.create(
                amount=stripe_total,
                currency="mxn",
                description=description,
                customer=customer.id,
            )
            try:
                order_details = Order.objects.create(
                    token=token,
                    total=total,
                    emailAddress=email,
                    billingName=billingName,
                    billingAddress1=billingAddress1,
                    billingCity=billingCity,
                    billingPostcode=billingPostcode,
                    billingCountry=billingCountry,
                    shippingName=shippingName,
                    shippingAddress1=shippingAddress1,
                    shippingCity=shippingCity,
                    shippingPostcode=shippingPostcode,
                    shippingCountry=shippingCountry,
                )
                order_details.save()
                for order_item in cart_items:
                    or_item = OrderItem.objects.create(
                        product=order_item.product.name,
                        quantity=order_item.quantity,
                        price=order_item.product.price,
                        order=order_details,
                    )
                    or_item.save()

                    # Reducir stock
                    products = Product.objects.get(id=order_item.product.id)
                    products.stock = int(order_item.product.stock - order_item.quantity)
                    products.save()
                    order_item.delete()

                    print("Orden Creada!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                return redirect("thanks_page", order_details.id)

            except ObjectDoesNotExist:
                pass

        except stripe.error.CardError as e:
            return False, e

    context = {
        "cart_items": cart_items,
        "total": total,
        "counter": counter,
        "stripe_total": stripe_total,
        "description": description,
        "data_key": data_key,
    }
    return render(request, "orders/cart.html", context)


def cart_remove(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = Product.objects.get(id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect("cart_detail")


def cart_delete_product(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = Product.objects.get(id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect("cart_detail")


def thankyou_page(request, order_id):
    if order_id:
        customer_order = Order.objects.get(id=order_id)

    context = {"customer_order": customer_order}
    return render(request, "orders/thankyou.html", context)


@login_required
def orderHistory(request):
    email = str(request.user.email)
    order_details = Order.objects.filter(emailAddress=email)
    context = {"order_details": order_details}
    return render(request, "orders/orders_list.html", context)


@login_required
def viewOrder(request, order_id):
    email = str(request.user.email)
    order = Order.objects.get(id=order_id, emailAddress=email)
    order_items = OrderItem.objects.filter(order=order)
    context = {"order": order, "order_items": order_items}
    return render(request, "orders/order_detail.html", context)
