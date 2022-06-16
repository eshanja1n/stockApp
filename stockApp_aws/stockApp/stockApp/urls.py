"""stockApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import include, path

from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings


from stock.views import (
    index,
    trial,
    search_view,
)

from account.views import (
    registration_view,
    logout_view,
    login_view,
    account_view,
    profile_view,
)

from post.views import (
    create_post,
    show_graph,
    delete_post_view,
)





urlpatterns = [
    path('', index, name="home"),
    path('trial/', trial, name="trial"),
    path('register/', registration_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('account/', account_view, name='account'),
    path('post/create/', create_post, name='create_post'),
    path('post/graphs/<str:hex>/', show_graph, name='graph'),
    path('account/<str:username>/', profile_view, name='profile'),
    path('search/', search_view, name='search'),
    path('delete/<int:id>', delete_post_view, name="delete"),
    path('admin/', admin.site.urls),
]

