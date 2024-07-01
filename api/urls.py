from django.contrib import admin
from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    ## shortenURL Endpoints
    path('shortenURL', views.urlAPI.as_view(),name='url-api'),
    ## List
    path('ShortURLList',views.ShortURLList.as_view(),name='short-url-list'),
    ## User Endpoints
    path('users', views.UserList.as_view(), ),
    path('users/<int:pk>', views.UserDetail.as_view(), name='user-detail'),
    ## Token
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('url/<str:pk>/', views.URLUpdateDelete.as_view(), name='url-update-delete')
]
