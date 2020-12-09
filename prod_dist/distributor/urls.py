from django.urls import path
from django.contrib import admin
from distributor import views

app_name = 'distributor'

urlpatterns = [
    path('<int:distributor_id>/',views.distributor_retailers,name='index'),
    path('<int:distributor_id>/edit/',views.distributor_edit,name='distributor_edit'),
    path('<int:distributor_id>/retailers/',views.distributor_retailers,name='distributor_retailers'),
    path('<int:distributor_id>/companies/',views.distributor_companies,name='distributor_companies'),
    path('<int:distributor_id>/retailer_remove/<int:retailer_id>/',views.distributor_retailer_remove,name='distributor_retailer_remove'),
]
