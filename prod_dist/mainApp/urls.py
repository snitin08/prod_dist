from django.contrib import admin
from django.urls import path
from mainApp.views import register_retailer,register_success

app_name = 'mainApp'

urlpatterns = [
    path('', register_retailer,name='register_retailer'),
    path('regiser/success/',register_success,name="register_success"),
]
