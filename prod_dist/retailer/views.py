from django.shortcuts import render, HttpResponse, redirect
from mainApp.models import Distributor, Retailer, Company
from django.db import IntegrityError
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

@retailerAuthenticated
def retailer_edit(request,retailer_id):
    if request.method=='GET':
        retailer = Retailer.objects.filter(id=retailer_id).first()
        data = {
            "first_name":retailer.first_name,
            "last_name":retailer.last_name,
            "gst_number":retailer.gst_number,
            "mobile":retailer.mobile,
            "address":retailer.address,
            "state":retailer.state,
            "city":retailer.city,
            "pincode":retailer.pincode,            
        }
        return render(request,'retailer/retailer_edit.html',{"data":data})
    else:
        retailer = Retailer.objects.filter(id=retailer_id)
        data = request.POST.dict()        
        del data['csrfmiddlewaretoken']     
        print(data)   
        try:
            retailer.update(
                **data            
            )
        except IntegrityError as e:
            messages = {}
            messages['gst'] = "GST number must be unique."
            return render(request,"retailer/retailer_edit.html",{
                "messages":messages,
                "data":data
            })
        return render(request,"retailer/retailer_edit.html",{
                "success":True,
                "data":data
            })
        
