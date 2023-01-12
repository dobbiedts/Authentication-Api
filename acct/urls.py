from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('register', RegisterAPI.as_view()),
    path('login', LoginView.as_view()),
    path('verify', VerifyOTP.as_view()),
    path('list_view', ListView.as_view()),
    path('user/<str:id>', UserView.as_view()),
    path('logout', LogOut.as_view()),
   
]
