from django.contrib import admin
from django.urls import path
from receipt import views

app_name = 'receipt'

urlpatterns = [
    path('create_receipt/',views.create_receipt,name='create_receipt'),
]