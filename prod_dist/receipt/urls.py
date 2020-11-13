from django.contrib import admin
from django.urls import path
from receipt import views

app_name = 'receipt'

urlpatterns = [
    path('create_receipt/',views.create_receipt,name='create_receipt'),
    path('receipt_list/',views.receipt_list,name='receipt_list'),
    path('receipt_detail/',views.receipt_detail,name='receipt_detail'),
    path('receipt_product_detail/',views.receipt_product_detail,name='receipt_product_detail'),
]