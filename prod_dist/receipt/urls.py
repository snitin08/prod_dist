from django.contrib import admin
from django.views.generic.base import TemplateView
from django.urls import path
from receipt import views

app_name = 'receipt'

urlpatterns = [
    path('create_receipt/',views.create_receipt,name='create_receipt'),
    path('request_receipt/',views.request_receipt,name='request_receipt'),
    path('request_receipt/distributor/<int:distributor_id>/',views.distributor_products,name='distributor_products'),
    path('request_receipt/company/<int:company_id>/',views.company_products,name='company_products'),
    path('receipt_product_detail/',views.receipt_product_detail,name='receipt_product_detail'),
    path('receipt_detail/<str:receipt_id>/',views.receipt_detail,name='receipt_detail'),
    path('receipt_list/',views.receipt_list,name='receipt_list'),
    path('receipt_stats',views.receipt_stats,name='receipt_stats'),
    path('access_denied/',views.access_denied,name='access_denied'),
    path('process_receipt/', views.process_receipt,name='process_receipt'),
    path('submit_receipt/', views.submit_receipt,name='submit_receipt')
]