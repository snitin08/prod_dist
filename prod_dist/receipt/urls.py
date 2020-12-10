from django.contrib import admin
from django.urls import path
from receipt import views

app_name = 'receipt'

urlpatterns = [
    path('create_receipt/',views.create_receipt,name='create_receipt'),
    path('request_receipt/',views.request_receipt,name='request_receipt'),
    path('distributor/<int:distributor_id>/products/',views.distributor_products,name='distributor_products'),
    path('receipt_product_detail/',views.receipt_product_detail,name='receipt_product_detail'),
    path('receipt_detail/',views.receipt_detail,name='receipt_detail'),
    path('receipt_list/',views.receipt_list,name='receipt_list'),
]