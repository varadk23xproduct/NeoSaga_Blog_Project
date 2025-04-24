"""
URL configuration for NEGO_SAGA_PROJECT project.

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
from django.urls import path
from BLOG import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("login/", views.ulogin, name="login"),
    path("register/", views.register, name="register"),
    path("logout/", views.ulogout, name="logout"),
    path("", views.home_page, name="home"),
    path("blogs/", views.blog_list, name="blog_list"),
    path("blogs/<int:blog_id>/", views.blog_detail, name="blog_detail"),
    path("blogs/create/", views.create_blog, name="create_blog"), 
     path("logout/", views.ulogout, name="logout"),  
     path('blog/<int:blog_id>/delete/', views.delete_blog, name='delete_blog'),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)