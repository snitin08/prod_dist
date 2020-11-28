from django.shortcuts import render

# Create your views here.
def distributor_edit(request):
    return render(request,'distributor/distributor_edit.html',{})

def distributor_retailers(request):
    return render(request,'distributor/distributor_retailers.html',{})

def distributor_companies(request):
    return render(request,'distributor/distributor_companies.html',{})