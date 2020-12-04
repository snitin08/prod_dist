from django.shortcuts import render, HttpResponse, redirect
from mainApp.models import Distributor, Retailer, Company
# Create your views here.
def retailerAuthenticated(function):
  
    def wrap(request, *args, **kwargs):   
        try:     
            if request.session.get('user'):            
                retailer = Retailer.objects.filter(id=kwargs['retailer_id']).first()
                if retailer:
                    if retailer.email == request.session['user']:           
                        return function(request, *args, **kwargs)
                    else:
                        return render(request,'general/404.html',{})
                else:
                    return render(request,'general/404.html',{})
            else:
                return redirect('mainApp:login')
        except:
            return redirect('mainApp:login')
    return wrap

@retailerAuthenticated
def retailer_distributors(request,retailer_id):
    retailer = Retailer.objects.get(id=retailer_id)
    associated_distributors = retailer.distributor_set.all()
    print(associated_distributors)
    return render(request,"retailer/retailer_distributors.html",{
        "associated_distributors":associated_distributors,
    })
