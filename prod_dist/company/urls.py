from django.contrib import admin
from django.urls import path
from company import views

app_name = 'company'

urlpatterns = [
    
    path('edit/<str:company_name>',views.company_edit,name='company_edit'),
    path('<str:company_name>/distributors/',views.company_distributors,name='company_distributors'),
    path('<str:company_name>/distributor/remove/<int:distributor_id>',views.company_distributor_remove,name='company_distributor_remove'),
    path('<str:company_name>/products/',views.company_product_list,name='company_product_list'),
    path('<str:company_name>/product/<int:product_id>/detail',views.company_product_detail,name='company_product_detail'),
    path('<str:company_name>/product/<int:product_id>/remove',views.company_product_remove,name='company_product_remove'),
]