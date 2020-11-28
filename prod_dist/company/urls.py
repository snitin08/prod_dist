from django.contrib import admin
from django.urls import path
from company import views

app_name = 'company'

urlpatterns = [
    path('edit/',views.company_edit,name='company_edit'),
    path('distributors/',views.company_distributors,name='company_distributors'),
    path('products/',views.company_product_list,name='company_product_list'),
    path('product/detail',views.company_product_detail,name='company_product_detail'),
]