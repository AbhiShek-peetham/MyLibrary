from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name='login_page'),
    path('registeruser/', views.registration_view, name='user_register'),
    path('admin_view/', views.admin_view, name='admin_view'),
    path('user_view/', views.user_view, name='user_view'),
    path('logout_view/', views.logout_view, name='logout_view'),


]