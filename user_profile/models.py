from django.db import models
from static_app.models import LoginTable,UserProfile,UsersModels 
from django.contrib.auth.models import User

# The "Cart" model represents a user’s cart as a whole, associating it with a user (LoginTable) 
# and the items (UsersModels) that might be added.
class Cart(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    items = models.ManyToManyField('static_app.UsersModels')

    
    def __str__(self):
        return "{}".format(self.items)
# user: This means each user can have only one Cart, and each Cart belongs to one specific user.
# items : Each Cart can have multiple items (books, in this case and if different users add the same book to their carts). 


# CartItem is used to manage each unique item in the cart.
class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    book = models.ForeignKey('static_app.UsersModels',on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return "{}".format(self.cart)
   
   