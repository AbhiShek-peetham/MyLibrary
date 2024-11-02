"""
URL configuration for static_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user_accounts.urls')),

    # path('', include('static_app.urls')),
    # path('login_page/', include('user_accounts.urls')),
    # path('user_base/', include('user_profile.urls')),

    path('dash_view/', include('static_app.urls')),
    path('user_base/', include('user_profile.urls')),
    
]

if settings.DEBUG: #This code block only runs if DEBUG is True, meaning it will only work in a development environment.

    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT) # serves static files like CSS, JavaScript, and images when DEBUG is True.
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) #This line serves media files, which are typically user-uploaded files, such as profile pictures and documents, in development.

# "settings.MEDIA_URL" defines the URL path for accessing media files (e.g., /media/).
# "settings.MEDIA_ROOT" is the directory on your filesystem where media files are stored.
# "settings.STATIC_ROOT" specifies the location where the static files are collected 
# when you run python manage.py collectstatic.