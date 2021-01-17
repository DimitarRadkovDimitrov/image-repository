from .views import *
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('login/', user_views.user_login),
    path('logout/', user_views.user_logout),
    path('users/', user_views.users),
    path('images/', image_views.images)
]
