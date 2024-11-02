from django.contrib import admin
from . models import UsersModels,LoginTable,UserProfile

# Register your models here.

admin.site.register(UsersModels),
admin.site.register(LoginTable),
admin.site.register(UserProfile),

