from django.contrib import admin
from .models import Company,Distributor,Retailer
# Register your models here.
admin.site.register(Company)
admin.site.register(Distributor)
admin.site.register(Retailer)
