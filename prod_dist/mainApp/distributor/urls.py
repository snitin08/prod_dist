from django.urls import path
from django.contrib import admin
from distributor import views

app_name = 'distributor'

urlpatterns = [
    path('edit/',views.distributor_edit,name='distributor_edit'),
    path('retailers/',views.distributor_retailers,name='distributor_retailers'),
    path('companies/',views.distributor_companies,name='distributor_companies'),
]