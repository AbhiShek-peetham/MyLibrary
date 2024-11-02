from django.urls import path 
from . import views
from django.contrib.auth.models import User

urlpatterns = [
    path('', views.dash_view,name="dash_view"),
    path('create/', views.create,name="create"),
    path('update/<int:user_id>/', views.update,name="update"),
    path('delete/<int:user_id>/', views.delete,name="delete"),
    path('view/', views.view,name="view"),
    path('search/', views.searchBooks,name="search"),
    path('base/', views.searchBooks,name="base"),
    path('register/', views.registerUser,name="register"),
    path('login/',views.loginUser,name = 'login'),
    path('logout/',views.logoutUser, name = "logout"),
    path('home/',views.homePage, name = "home"),


]