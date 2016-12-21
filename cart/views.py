from django.shortcuts import render
from . import cart
from django.http import HttpResponseRedirect
from checkout import checkout
from skart import settings


def show_cart(request, template_name='cart/cart.html'):
    if request.method == 'POST':
        postdata = request.POST.copy()
        if postdata['submit'] == 'Remove':
            cart.remove_from_cart(request)
        if postdata['submit'] == 'Update':
            cart.update_cart(request)
        if postdata['submit'] == 'Checkout':
            checkout_url = checkout.get_checkout_url(request)
            return HttpResponseRedirect(checkout_url)
    cart_items = cart.get_cart_items(request)
    page_title = 'Shopping Cart'
    cart_subtotal = cart.cart_subtotal(request)
    # for Google Checkout button
    merchant_id = settings.GOOGLE_CHECKOUT_MERCHANT_ID
    return render(request, template_name, locals())
