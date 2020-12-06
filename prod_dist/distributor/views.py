from django.shortcuts import render, HttpResponse, redirect
from mainApp.models import Distributor, Retailer, Company
# Create your views here.
def distributorAuthenticated(function):
  
    def wrap(request, *args, **kwargs):   
        try:     
            if request.session['user']:            
                distributor = Distributor.objects.filter(id=kwargs['distributor_id']).first()
                if distributor:
                    if distributor.email == request.session['user']:           
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

@distributorAuthenticated
def distributor_edit(request,distributor_id):
    if request.method=='GET':
        distributor = Distributor.objects.filter(id=distributor_id).first()

        return render(request,'distributor/distributor_edit.html',{
            "data":distributor
        })
    else:
        data = request.POST
        #print(data)
        first_name = data.get('first name')
        last_name = data.get('Last name')
        mobile = data.get('Mobile')
        address = data.get('address')
        state = data.get('state')
        city = data.get('city')
        pincode = data.get('pincode')

        distributor = Distributor.objects.filter(id=distributor_id)
        distributor.update(
            first_name=first_name,
            last_name=last_name,
            mobile=mobile,
            address=address,
            state=state,
            city=city,
            pincode=pincode
        )

        return redirect('distributor:distributor_edit',distributor_id=distributor_id)


@distributorAuthenticated
def distributor_retailers(request,distributor_id):
    if request.method=='GET':
        distributor = Distributor.objects.filter(id=distributor_id).first()
        associated_retailers = distributor.distributor_retailers.all()
        non_associated_retailers = Retailer.objects.exclude(id__in=associated_retailers)
        return render(request,'distributor/distributor_retailers.html',{
            "associated_retailers":associated_retailers,
            "non_associated_retailers":non_associated_retailers,
            "distributor":distributor
        })
    else:
        data = request.POST
        print(data)
        retailer_id = int(data.get("add_retailer_id"))
        retailer = Retailer.objects.get(id=retailer_id)
        distributor = Distributor.objects.filter(id=distributor_id).first()
        distributor.distributor_retailers.add(retailer)
        return redirect('distributor:distributor_retailers',distributor_id=distributor_id)

@distributorAuthenticated
def distributor_retailer_remove(request,distributor_id,retailer_id):
    distributor = Distributor.objects.filter(id=distributor_id).first()
    retailer = Retailer.objects.get(id=retailer_id)
    distributor.distributor_retailers.remove(retailer)
    return redirect('distributor:distributor_retailers',distributor_id=distributor_id)


@distributorAuthenticated
def distributor_companies(request,distributor_id):
    distributor = Distributor.objects.get(id=distributor_id)
    distributor_companies = distributor.company_set.all()
    return render(request,'distributor/distributor_companies.html',{
        "associated_companies":distributor_companies,
        "distributor":distributor,
    })