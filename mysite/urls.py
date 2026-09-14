"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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

    Leaving this in the code intentionally for future use and callback
"""
"""
Root URL Configuration for the 'mysite' Django project.
Includes app-level routing modules into the top-level URL dispatcher.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Built-in Django administrative panel interface
    path('admin/', admin.site.urls),
    
    # Delegates all root paths directly to the core application's urls.py
    path('', include('core.urls')),
]