from django.contrib import admin
from django.urls import path
from mainApp.views import register_retailer,register_success, index
from mainApp import views
from django.views.generic.base import TemplateView


app_name = 'mainApp'

urlpatterns = [
    path('',index,name='index'),
    path('register/company/', views.register_company,name='register_company'),
    path('register/distributor/', views.register_distributor,name='register_distributor'),
    path('register/retailer/', register_retailer,name='register_retailer'),
    path('regiser/success/',register_success,name="register_success"),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('create_data',views.createData,name='create_data'),
    path('404/',TemplateView.as_view(template_name='general/404.html'),name='404'),
]
