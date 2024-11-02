from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_profile_view, name='user_base'),  # Ensure this list is not empty
    path("lists_view/", views.lists_view, name='lists_view'),
    path("user_search/", views.userSearchBooks, name='user_search'),
    path('add_to_cart/<int:book_id>/',views.add_to_cart, name="addtocart"),
    path("viewcart/",views.view_cart,name="viewcart"),
    path('increase_quantity/<int:item_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:item_id>/', views.decrease_quantity, name='decrease_quantity'),
    path('remove-from-cart/<int:item_id>/',views.remove_from_cart,name='remove_cart'),
    path('create-checkout-session/',views.create_checkout_session,name="create_checkout_session"),
    path('success/',views.success,name="success"),
    path('cancel/',views.cancel,name="cancel")

]
