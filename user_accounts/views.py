from django.shortcuts import render,redirect
from django.http import HttpResponse
from static_app.models import UserProfile,LoginTable
from django.contrib import messages,auth
from django.contrib.auth import logout,login,authenticate
from django.contrib.auth.models import User
from django.db.models import Q



# Create your views here.

def login_view(request):
    # print("Login view is called!!")

    return render(request,'user_login.html')


def registration_view(request):
    print("registration view is called!!")
      # Instantiate new instances of the models
    login_table = LoginTable() #store essential authentication information, such as username, password, and type.
    user_profile = UserProfile() #hold additional user details that are not directly related to logging in, such as personal information (e.g., name, contact information, address).

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        cpassword = request.POST.get('cpassword')

        user_profile.username = username # if the registration is successfull, then this command will save it to db user_profile.save()
        user_profile.password = password # 

        login_table.username = username
        login_table.password = password
        login_table.type = 'user' #field indicates the user’s role, which could be helpful if the application has different types of users (e.g., admins, regular users, etc.).

        if password == cpassword:
            # print("User profile is called",user_profile)
            # print("login table is called",login_table)

            user_profile.save()
            login_table.save()
            messages.info(request,'registration successful')
            return redirect('login_page')
        
        else:
            messages.warning(request,'password do not match')
            return redirect('user_register')

    return render(request,'user_register.html')

def login_page(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user_exists = LoginTable.objects.filter(Q(username=username) & Q(password=password) & 
                                                (Q(type="user")|Q(type="admin"))).exists()

        #checks if a record exists with matching credentials and type='user' or "admin".
        # user = LoginTable.objects.filter(username=username,password=password,type='user').exists()
        # print("user is called",user) # if exists, user will be True, else False
        try:
            if user_exists:
                user_details = LoginTable.objects.get(username=username, password=password)
                user_name = user_details.username
                user_type = user_details.type

                if user_type == 'user':
                    # Check if a corresponding Django User exists, and create if not
                    user, created = User.objects.get_or_create(username=user_name)
                    
                    # Log the user into Django's auth system
                    login(request, user)
                    request.session['username'] = user_name

                    print("User login successful:", request.user.is_authenticated)
                    
                    return redirect('user_view')
                
                elif user_type == 'admin':
                    
                    print("Admin is called:", request.user.is_authenticated)

                    # Similarly, create or get an admin user
                    admin_user, created = User.objects.get_or_create(username=user_name, is_staff=True, is_superuser=True)
                    login(request, admin_user)
                    request.session['username'] = user_name
                    return redirect('admin_view')
            else:
                messages.error(request, "invalid username or password")
        except:
            messages.error(request, 'Invalid Credentials!!')

    return render(request,'user_login.html')



def admin_view(request):
    user_name = request.session.get('username') # for session, it used request.session.get() in views to avoid errors if the session key is missing.
    return render(request, "base.html",{'user_name': user_name})

def user_view(request):
    print("user view is called")
    user_name = request.session.get('username') # Same here
    return render(request, "user_base.html",{'user_name': user_name})

def logout_view(request):
    logout(request)
    return redirect("login_page")
                
