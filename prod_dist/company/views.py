from django.shortcuts import render, HttpResponse, redirect
from mainApp.models import Company, Distributor, Retailer

# Create your views here.
def company_edit(request,company_name):

    if request.method=='POST':
        data = request.POST
        print(data)
        company_name = data.get('company name')
        mobile = data.get('Mobile')
        address = data.get('address')
        state = data.get('state')
        city = data.get('city')
        pincode = data.get('pincode')              

        collected_data = {
            "company_name":company_name,            
            "mobile":mobile,
            "address":address,
            "state":state,
            "city":city,
            "pincode":pincode,                       
        }
        company = Company.objects.filter(company_name = company_name)
        company.update(company_name=company_name,mobile=mobile,address=address,state=state, city=city, pincode=pincode)

        return HttpResponse('<h1>Update success</h1>')
        
        
    else:
        company = Company.objects.filter(company_name = company_name).first()
        #print(company.values())
        if company:
            data = {}
            data['company_name'] = company.company_name
            data['mobile'] = company.mobile
            data['address'] = company.address
            data['state'] = company.state 
            data['city'] = company.city
            data['pincode'] = company.pincode

            return render(request,'company/company_edit.html',{"data":data})
        """
        else:
            redirect 404 page
        """

def company_distributors(request,company_name):
    if request.method=='GET':
        company = Company.objects.get(company_name=company_name)
        company_distributors_list = company.company_distributors.all()
        non_company_distributors_list = Distributor.objects.exclude(id__in=company_distributors_list)
        print(company_distributors_list)
        print(non_company_distributors_list)
        return render(request,'company/company_distributors.html',{
            "existing_distributors":company_distributors_list,
            "non_associated_distributors":non_company_distributors_list,
            "company_name":company.company_name
            })
    else:
        data = request.POST
        print(data)
        add_distributor_id = int(data.get('add_distributor_id'))
        distributor = Distributor.objects.get(id=add_distributor_id)
        company = Company.objects.get(company_name=company_name)
        company.company_distributors.add(distributor)

        return redirect('company:company_distributors',company_name = company.company_name)

def company_distributor_remove(request,company_name,distributor_id):
    distributor = Distributor.objects.get(id=distributor_id)
    company = Company.objects.get(company_name=company_name)
    company.company_distributors.remove(distributor)
    return redirect('company:company_distributors',company_name = company_name)

def company_product_list(request):
    return render(request,'company/company_product_list.html',{})

def company_product_detail(request):
    return render(request,'company/company_product_detail.html',{})