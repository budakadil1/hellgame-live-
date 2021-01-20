'''This was an old cart function that was implemented with local sessions. I decided to
use user-based carts because it allows for saving of the cart data. '''




# change cart from session based to user 
def get_cart(request):
    # get session id. create one if non existent
    try: 
        session_id = request.session['cart_id']
    except:
        new_cart = Cart()
        new_cart.save()
        request.session['cart_id'] = new_cart.id
        session_id = new_cart.id
    # if session id is found, get cart from session_id as session_cart
    if session_id:
        try:
            session_cart = Cart.objects.get(id=session_id)
            # if for some reason cart is not found while session_id is, create new cart with except clause.
        except:
            new_cart = Cart()
            new_cart.save()
            request.session['cart_id'] = new_cart.id
            session_id = new_cart.id
            session_cart = Cart.objects.get(id=session_id)

    # set context_cart to none if session_id is empty.
    else:
        context_cart = None
    total_value = 0 
    if session_cart != None:
        context_cart = session_cart.products.all()
    for i in context_cart:
        total_value += i.price
        

    context = {"cart":context_cart, "total":total_value}
    template = "shoppingcart/cart_view.html"
    return render(request, template, context)

def add_to_cart(request, slug):
    # adds or removes product object.
    # get session cart, if not found, create one.
    try: 
        session_id = request.session['cart_id']
        cart = Cart.objects.get(id=session_id)
    except Cart.DoesNotExist:
        cart = Cart.objects.create(id=session_id)
        request.session['cart_id'] = cart.id
    except:
        cart = Cart()
        cart.save()
        request.session['cart_id'] = cart.id
        session_id = cart.id
    # get products inside cart if existing
    try:
        product = gamePost.objects.get(slug=slug)
    except gamePost.DoesNotExist:
        return HttpResponse("404. Please contact system admin.")
    except:
        print('Unknown exception at cart view - cart:views.py:62')
    if not product in cart.products.all():
        cart.products.add(product)
    # implement remove from cart function.
    else:
        cart.products.remove(product)
    
    #save total amount
    total_amount = 0
    for item in cart.products.all():
        total_amount += item.price
    cart.total = total_amount
    cart.save()
    
    return HttpResponseRedirect(reverse("shoppingcart:get_cart"))
   
# new remove_from_cart function.
def remove_from_cart(request, slug):
    return HttpResponse('remove from cart.')