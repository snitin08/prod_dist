from django.shortcuts import render

# Create your views here.
def company_edit(request):
    return render(request,'company/company_edit.html',{})

def company_distributors(request):
    return render(request,'company/company_distributors.html',{})

def company_product_list(request):
    return render(request,'company/company_product_list.html',{})

def company_product_detail(request):
    return render(request,'company/company_product_detail.html',{})