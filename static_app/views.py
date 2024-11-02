from django.shortcuts import render,redirect,get_object_or_404
from . import models 
from django.http import HttpResponse,Http404
from . models import UsersModels,UserProfile
from django.contrib import messages,auth
from django.core.paginator import Paginator,EmptyPage
from  django.db.models import Q
from django.db import connection
from django.contrib.auth.models import User
# from django.contrib.auth import logout




# Create your views here.

def list_book(request):
    book_list = UsersModels.objects.all()
    return render(request,'base.html',{'book_list':book_list})


def create(request):
    if request.method == "POST":
        name_user = request.POST.get("create_name")
        email_user = request.POST.get("create_email")
        author_user = request.POST.get("create_author")
        price_user = request.POST.get("create_price")
        user_obj = UsersModels(name_db=name_user,email_db = email_user,author_db=author_user,price_db=price_user)
        user_obj.save()
        messages.success(request, 'Book created successfully!') # for message alert
        return redirect('create')

    return render(request,"create.html",)

def base(request):
    return render(request,"base.html")

# def update(request,user_id):
#     update_obj = None

def update(request, user_id):
    # using exception method to redirect the page to those available user_id after the deletion happens.
    # try:
    #     update_obj = UsersModels.objects.get(id=user_id)
    # except UsersModels.DoesNotExist:
    #     print("current user is called",request.user)
    #     messages.error(request,"The user doesn't exist")
    #     return redirect('update')
    
    # Find the first available user
    # first_user = UsersModels.objects.order_by('id').first()
    # if first_user:
    #     return redirect(f'update/{first_user.id}/')

    update_obj = UsersModels.objects.get(id=user_id)
   
    # print("ID is called :",id) # ID is called : <built-in function id>
    if request.method =='POST':
        name_update = request.POST.get("name_update")
        email_update = request.POST.get("email_update")
        author_update = request.POST.get("author_update")
        price_update = request.POST.get("price_update")
        quantity = request.POST.get("quantity")

        update_obj.name_db = name_update
        update_obj.email_db = email_update
        update_obj.author_db = author_update
        update_obj.price_db = price_update
        update_obj.quantity = quantity


        update_obj.save()
        messages.success(request, 'Book updated successfully!') # for message alert
        return redirect('view')

    return render(request, 'update.html', {'update_dic':update_obj})


def delete(request,user_id):
    # try:
    #     delet_obj = UsersModels.objects.get(id=user_id)
    # except UsersModels.DoesNotExist:
    # # Find the first available user
    #     first_user = UsersModels.objects.order_by('id').first()
    #     if first_user:
    #         return redirect(f'delete/{first_user.id}/')
    #     else:
    #         raise Http404("No users available")
        
    delete_obj1 = UsersModels.objects.get(id=user_id)
    if request.method =='POST':
        delete_obj1.delete()
        messages.success(request, 'User deleted successfully!') # for message alert
        return redirect('view')

    return render(request,"delete.html",{"users":delete_obj1})

def view(request):
    # print("view is called!") 

    view_key = UsersModels.objects.all() # All db items you want to paginate
    paginator = Paginator(view_key,10)  # Create a Paginator object with 4 items per page
    page_number = request.GET.get('page') # Get the current page number from the GET parameters
    

    try:
        page = paginator.get_page(page_number) # Get the objects for the current page

    except EmptyPage: # if there are no pages, show an empty page
        page = paginator.page(page_number.num_pages)

    return render(request,"view.html",{'view_key':view_key,'page':page}) # Pass the page object to the template

def dash_view(request):
    view_key = UsersModels.objects.all() 
    paginator = Paginator(view_key,10)  
    page_number = request.GET.get('page') 
    # print("dash_view is called!",page_number)

    try:
        page = paginator.get_page(page_number) 
        print("try is called!",page) # <Page 1 of 2> if the page is on first page

    except EmptyPage: 
        page = paginator.page(page_number.num_pages)
        print("Exception is called!",page)

    return render(request,"base.html",{'view_key':view_key,'page':page})

def searchBooks(request):
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
    return render(request,"base.html", search_dict)

def registerUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        cpassword = request.POST.get('confirm_password')

        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request,' This user name already exists!')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'This email id is already taken!')
                return redirect('register')

            else: 
                user= User.objects.create_user(username=username,first_name = first_name,last_name=last_name,email=email,password=password)
                user.save()
                messages.info(request,'Your signup was successfull!')
                return redirect('login')
        else:
            messages.info(request,"This password doesn't match")
            return redirect('register')

    return render(request,'register.html')


def loginUser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username,password=password) # checking user is authenticated
        # print("user is called",user)
        if user is not None: # if the user is already registered
            auth.login(request,user) # 
            return redirect('dash_view')
        else:
            messages.error(request,"Invalid login credential!")
            return redirect('login')
    return render(request,"login.html")

def logoutUser(request):
    auth.logout(request)
    messages.warning(request,"You have successfully logged out")
    return redirect('login')
        
def homePage(request):
    return render(request,'home.html')

# Role based authentication(User / Admin) 

def userRegistrtion(request):
    userprofile = UserProfile()
    login_table = UserProfile()

    if request.method == "POST":
        userprofile.username = request.POST('username')
        userprofile.password = request.POST('password')
        userprofile.password2 = request.POST('password2')




