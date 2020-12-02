from django.contrib import admin
from django.urls import path
from accounts.views import HomePageView
from accounts import views

app_name = 'accounts'

urlpatterns = [
    path('',HomePageView.as_view(),name='home'),
    path('signup/',views.singuppage,name='signup'),
    path('login/',views.userlogin,name='login'),
    path('logout/',views.userlogout,name='logout')
]
