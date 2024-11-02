from django.db import models


# Create your models here.

class UsersModels(models.Model):
    name_db = models.CharField(max_length=100)
    email_db = models.CharField(max_length=100)
    author_db = models.CharField(max_length=100)
    quantity = models.IntegerField()
    price_db = models.IntegerField()
    img = models.ImageField(upload_to="books")

    def __str__(self):
        return '{}'.format(self.name_db)
    
    def __str__(self):
        return '{}'.format(self.author_db)


class UserProfile(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    password2 = models.CharField(max_length=200)

    def __str__(self):
        return '{}'.format(self.username)

class LoginTable(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    password2 = models.CharField(max_length=200)
    type = models.CharField(max_length=200)

    def __str__(self):
        return '{}'.format(self.username)
    

