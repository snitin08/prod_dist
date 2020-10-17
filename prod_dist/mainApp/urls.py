from django.contrib import admin
from django.urls import path
from mainApp.views import register_retailer,register_success, index
from mainApp import views

app_name = 'mainApp'

urlpatterns = [
    path('',index,name='index'),
    path('register/company/', views.register_company,name='register_company'),
    path('register/distributor/', views.register_distributor,name='register_distributor'),
    path('register/retailer/', register_retailer,name='register_retailer'),
    path('regiser/success/',register_success,name="register_success"),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),

    path('test_page/',views.test_page,name='test_page'),
]
