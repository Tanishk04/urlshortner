from django.contrib import admin
from django.urls import path, include
from api.views import URLRedirection
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("shortenURL/", views.shorten_url, name="shortenURL" ),
    path('url-list/', views.url_list, name='url_list'),
    path('url_update/<str:alias>', views.update_url, name='url_update'),
    path('url_delete/<str:alias>', views.delete_url, name='url_delete'),
    path('<str:alias>', views.my_redirect, name='my_redirect'),
    
    
]
