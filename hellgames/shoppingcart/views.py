from django.shortcuts import render, HttpResponseRedirect, HttpResponse, get_object_or_404
from django.urls import reverse
from accounts.models import gamePost
from .models import Cart
from django.http import Http404
from django.contrib import messages
from django.contrib.auth import get_user_model
CustomUser = get_user_model()
from django.contrib.auth.decorators import login_required
# change cart from session based to user 

@login_required
def get_cart(request):
    try:
        user_context = request.user
    except User.DoesNotExist:
        print('No user at shoppingcart')
        raise Http404
    # get cart associated to user
    cartObj, created = Cart.objects.get_or_create(user=request.user)
    cart_context = cartObj.products.all()
    cart_total_context = cartObj.total_price['total_price']
    
    context = {"cart":cart_context, "cart_total":cart_total_context}
    return render(request, "shoppingcart/cart_view.html", context)

@login_required
def add_to_cart(request, slug):
    try:
        user_context = request.user
    except User.DoesNotExist:
        print('No user at shoppingcart')
        raise Http404
    cartObj = get_object_or_404(Cart, user=user_context)
    try:
        product = gamePost.objects.get(slug=slug)
    except gamePost.DoesNotExist:
        print('No gamePost')
        raise Http404
    # bad logic
    if not product in cartObj.products.all():
        cartObj.products.add(product)
        cartObj.save()
    else:
        pass
        #messages.warning(request, "This item already exists in your cart. If this is a mistake, please contact the system admin.")
    
    return HttpResponseRedirect(reverse("shoppingcart:get_cart"))

@login_required
def remove_from_cart(request, slug):
    try:
        user_context = request.user
    except User.DoesNotExist:
        print('No user at shoppingcart')
        raise Http404
    
    cartObj = get_object_or_404(Cart, user=user_context)
    try:
        product = gamePost.objects.get(slug=slug)
    except gamePost.DoesNotExist:
        print('no GamePost')
        raise Http404
    # bad logic 
    if product in cartObj.products.all():
        cartObj.products.remove(product)
    else:
        messages.warning(request, "This item does not exist in your cart. If this is a mistake, please contact the system admin.")
    
    return HttpResponseRedirect(reverse("shoppingcart:get_cart"))
    


