from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from static_app.models import UserProfile,LoginTable,UsersModels
from user_profile.models import Cart,CartItem
from  django.db.models import Q
from django.contrib.auth.models import User
import stripe
from django.conf import settings
from django.urls import reverse
from django.http import JsonResponse

stripe_api_key = settings.STRIPE_SECRET_KEY



# Create your views here.

def user_profile_view(request):
    return render(request,'user_base.html')

def lists_view(request):
    books = UsersModels.objects.all()
    return render(request,'lists_view.html',{'books':books})

def userSearchBooks(request):
    query = None
    books = None
    if "q" in request.GET:
        query = request.GET.get('q')
        # print("Query is :::",query)
        books = UsersModels.objects.filter(Q(name_db__icontains = query)|Q(author_db__icontains = query)) # Q module is inheriting from models for searching
        # print("Search result is",books)
    else:
        books = []
    
    search_dict={
        'query' : query, 
        'books' : books, 
    }
    return render(request,"lists_view.html", search_dict)


def add_to_cart(request,book_id): 
    book = get_object_or_404(UsersModels, id=book_id) #get_object_or_404, checks the specific parameter is in the db, otherwise raises 404 error
    # book = UsersModels.get(id=book_id) # tis will not raise an error
    
    if book.quantity >0: # Checks if the book has a quantity greater than 0

        # "cart" holds the Cart object (either existing or newly created).
        # "created" tells us whether a new Cart had to be created (True) or if an existing one was found (False).
        print("Request user:", request.user) # check the user is authenticated

        cart,created = Cart.objects.get_or_create(user=request.user)  #If so, it gets or creates a Cart instance associated with the request.user.
        print("cart user is called", cart,created)

        # If the user doesn't already have a cart, a new one is created.
        
        # It then either fetches or creates a CartItem for this specific book within the user's cart.
        cart_item,item_created = CartItem.objects.get_or_create(cart=cart,book=book)
        print("cart ITEM is called", cart_item,item_created)

        
        if not item_created: #If the CartItem was(the same item added before ) already in the cart (i.e., item_created is False), it increases the CartItem's quantity by 1 and saves it.
            cart_item.quantity+=1
            cart_item.save() # saves to the db CartItem within the row that corresponds to this cart_item

    return redirect('viewcart')


def view_cart(request):

    # Get or create the cart for the authenticated user
     
    cart,created = Cart.objects.get_or_create(user=request.user) # This function retrieves the cart for the user, creating a new one if necessary.
    cart_items = cart.cartitem_set.all() #'cartitem_set' is Django's default way, which will Get all items in this cart
    total_price = sum(item.book.price_db * item.quantity for item in cart_items) # calculates the total cost of all items
    total_items = cart_items.count() #counts the number of items in the cart.

    # print("cart items called",cart_items)
    # print("cart item called",cart_item)
    # print("cart price called",total_price)
    # print("total items called",total_items)

    context = {
        'cart_items':cart_items,
        'total_price': total_price,
        'total_items': total_items
    }

    return render(request,'cart.html',context)

def increase_quantity(request,item_id):
    # cart_item = CartItem.objects.get(id = item_id)
    cart_item = get_object_or_404(CartItem, id=item_id)

    if cart_item.quantity < cart_item.book.quantity: # only if it less than the stock from db
        cart_item.quantity +=1
        cart_item.save()

    return redirect('viewcart')
    

def decrease_quantity(request,item_id):
    # cart_item = CartItem.objects.get(id = item_id)
    cart_item = get_object_or_404(CartItem, id=item_id)
     
    if cart_item.quantity > 1:
        cart_item.quantity -=1
        cart_item.save()
        
    return redirect('viewcart')

def remove_from_cart(request,item_id):
    try:
        cart_item = CartItem.objects.get(id=item_id)
        cart_item.delete()
    except cart_item.DoesNotExist:
        pass

    return redirect('viewcart')
    
def create_checkout_session(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    cart_items = CartItem.objects.all()

    if cart_items:

        if request.method == 'POST':
            line_items = []
            for cart_item in cart_items:
                if cart_item.book and cart_item.book.price_db is not None:
                    line_item={
                        'price_data':{
                         "currency":'usd',
                         'unit_amount':int(cart_item.book.price_db * 100),
                         'product_data':{
                             'name':cart_item.book.name_db
                         },

                     },
                    'quantity':1
                }
                line_items.append(line_item)

            if line_items:
                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=line_items,
                    mode='payment',
                    success_url=request.build_absolute_uri(reverse('success')),
                    cancel_url=request.build_absolute_uri(reverse('cancel'))
                )

                return redirect(checkout_session.url,code=303)
            
    return JsonResponse({'error': 'Invalid request'}, status=400)


def success(request):
    cart_items = CartItem.objects.all()

    for cart_item in cart_items:
        product = cart_item.book
                                # cart_item.quantity: This field holds the quantity of the specific book that was added to the cart.
        if product.quantity >= cart_item.quantity: # whether there is enough stock (product.quantity) to fulfill the requested quantity
            product.quantity-= cart_item.quantity # If the stock is sufficient, product.quantity -= cart_item.quantity reduces the stock by the ordered quantity,
            product.save()

    cart_items.delete() #deletes all CartItem entries from the database. Ensuring it’s empty once the order is complete.

    return render(request,'success.html')

def cancel(request):
    return render(request,'cancel.html')    