from django.shortcuts import render
from django.shortcuts import render, HttpResponse, redirect
from mainApp.models import Company, Distributor, Retailer, CompanyProducts
from functools import wraps
from django.db import IntegrityError

# Create your views here.
def CompanyAuthenticated(function):
  
    def wrap(request, *args, **kwargs):   
        try:     
            if request.session['user']:
                company = Company.objects.filter(company_name=kwargs['company_name']).first()
                if company:
                    if company.email == request.session['user']:           
                        return function(request, *args, **kwargs)
                    else:
                        return render(request,'general/404.html',{})
                else:
                    return redirect('mainApp:404')
            else:
                return redirect('mainApp:login')
        except:
            return redirect('mainApp:login')
    return wrap

@CompanyAuthenticated
def company_edit(request,company_name):
    company = Company.objects.get(company_name=company_name)
    if company.email==request.session['user']:
        if request.method=='POST':
            data = request.POST.dict()
            print(data)
            del data['csrfmiddlewaretoken']
            company_name = data['company_name']
            company = Company.objects.filter(company_name = company_name)
            try:
                company.update(**data)
            except IntegrityError as e:
                messages = {}
                print(str(e))
                if str(e)=="UNIQUE constraint failed: mainApp_address.address":
                    messages['address'] = "Address must be unique"
                elif str(e)=="UNIQUE constraint failed: mainApp_pincode.pincode":
                    messages['pincode'] = "Pincode already belongs to different city"
                elif str(e)=="UNIQUE constraint failed: mainApp_address.address":
                    messages['address'] = "Address must be unique"
                else:
                    messages['gst'] = "GST number must be unique. Check your GST number."
                return render(request,'company/company_edit.html',{
                    "data":data,
                    "messages":messages,
                })

            return render(request,"company/company_edit.html",{
                "data":data,
                "success":True
            })
            
            
        else:
            company = Company.objects.filter(company_name = company_name).first()
            #print(company.values())
            if company:
                data = {}
                data['company_name'] = company.company_name
                data['mobile'] = company.mobile
                data['address'] = company.address.address
                data['state'] = company.address.pincode.city.state 
                data['city'] = company.address.pincode.city.city
                data['pincode'] = company.address.pincode.pincode
                data['gst_number'] = company.gst_number

                return render(request,'company/company_edit.html',{"data":data})
            """
            else:
                redirect 404 page
            """
    else:
        return HttpResponse('<h1>Access denied</h1>')

@CompanyAuthenticated
def company_distributors(request,company_name):
    company = Company.objects.get(company_name=company_name)
    if company.email==request.session['user']:
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
    else:
        return HttpResponse('<h1>Access denied</h1>')


@CompanyAuthenticated
def company_distributor_remove(request,company_name,distributor_id):
    company = Company.objects.get(company_name=company_name)
    if company.email==request.session['user']:
        distributor = Distributor.objects.get(id=distributor_id)
        company = Company.objects.get(company_name=company_name)
        company.company_distributors.remove(distributor)
        return redirect('company:company_distributors',company_name = company_name)
    else:
        return HttpResponse('<h1>Access denied</h1>')

@CompanyAuthenticated
def company_product_list(request,company_name):
    company = Company.objects.get(company_name=company_name)
    if company.email==request.session['user']:
        if request.method=='GET':
            company = Company.objects.get(company_name=company_name)
            if company:
                company_products = company.companyproducts_set.all()
                #print(company_products)
                return render(request,'company/company_product_list.html',{
                    "company_products":company_products,
                    "company_name":company_name,
                })

            else:
                return HttpResponse('<h1>No company found</h1>')
        else:
            data = request.POST.dict()
            del data['csrfmiddlewaretoken']
            print(data)        
            company = Company.objects.get(company_name=company_name)
            total_tax = float(data['cg_gst'])+float(data['sg_gst'])
            CompanyProducts.objects.create(
                **data,product_company=company,total_tax=total_tax
            )
            return redirect('company:company_product_list',company_name=company_name)
    else:
        return HttpResponse('<h1>Access denied </h1>')

@CompanyAuthenticated
def company_product_remove(request,company_name,product_id):
    company = Company.objects.get(company_name=company_name)
    if company.email==request.session['user']:
        CompanyProducts.objects.get(id=product_id).delete()
        return redirect('company:company_product_list',company_name=company_name)
    else:
        return HttpResponse('<h1>Access denied </h1>')

@CompanyAuthenticated
def company_product_detail(request,company_name,product_id):

    if request.method=='GET':
        product = CompanyProducts.objects.filter(id=product_id).first()
        
        if product:
            
            if not str(product.product_company)==company_name:
                return HttpResponse("<h1>Access denied</h1>")
            else:
                return render(request,'company/company_product_detail.html',{
                    "product":product,
                    "company_name":company_name
                })
        else:
            return HttpResponse("<h1>No product found</h1>")
    else:
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']
        print(data)

        product = CompanyProducts.objects.filter(id=product_id)
        
        if product.first():
            
            if not str(product.first().product_company)==company_name:
                return HttpResponse("<h1>Access denied</h1>")
            else:
                sg = float(data['sg_gst'])
                cg = float(data['cg_gst'])
                product.update(
                    **data,total_tax=sg+cg
                )
                return redirect('company:company_product_list',company_name=company_name)
        else:
            return HttpResponse("<h1>No product found</h1>")



        
