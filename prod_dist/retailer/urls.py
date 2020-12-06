from django.urls import path
from django.contrib import admin
from retailer import views

app_name = 'retailer'

urlpatterns = [
    path("<int:retailer_id>/distributors/",views.retailer_distributors,name='retailer_distributors'),
]