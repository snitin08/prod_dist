from django.urls import path
from django.contrib import admin
from retailer import views

app_name = 'retailer'

urlpatterns = [
    path('<int:retailer_id>/',views.retailer_distributors,name='index'),
    path("<int:retailer_id>/distributors/",views.retailer_distributors,name='retailer_distributors'),
    path('<int:retailer_id>/edit/',views.retailer_edit,name='retailer_edit'),
    
]