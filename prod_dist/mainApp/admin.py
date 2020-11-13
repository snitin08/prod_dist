from django.contrib import admin
from .models import Company,Distributor,Retailer,CompanyProducts
# Register your models here.
admin.site.register(Company)
admin.site.register(Distributor)
admin.site.register(Retailer)
admin.site.register(CompanyProducts)