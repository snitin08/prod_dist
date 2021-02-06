from django.contrib import admin
from .models import Company,Distributor,Retailer,CompanyProducts,City,Pincode,Address
# Register your models here.
admin.site.register(Company)
admin.site.register(City)
admin.site.register(Pincode)
admin.site.register(Address)
admin.site.register(Distributor)
admin.site.register(Retailer)
admin.site.register(CompanyProducts)