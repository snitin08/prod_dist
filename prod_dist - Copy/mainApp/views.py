from django.shortcuts import render, HttpResponse, redirect
from .models import Company,Distributor,Retailer
from .models import CustomBackend
from django.contrib.auth import login,logout
from .fill_data import *
from django.db import IntegrityError

def notAuthenticated(function):

    def wrap(request,*args,**kwargs):
        if request.session.get('user'):
            t = request.session.get('type')
            if t=='company':
                return redirect('company:company_product_list',company_name=request.session['company_name'])
            elif t=='distributor':
                return redirect('distributor:distributor_retailers',distributor_id=request.session['id'])
            elif t=='retailer':
                return redirect('retailer:retailer_distributors',retailer_id=request.session['id'])
        else:
            return function(request,*args,**kwargs)
    return wrap

#Create your views here.
def createData(request):
    createCompany(5)
    createDistributor(5)
    createRetailer(5)
    return redirect('mainApp:index')

@notAuthenticated
def index(request):
    if not request.session.get('user'):
        print(request.session.get('user'))
        return render(request,'auth/index.html',{})
        
@notAuthenticated
def register_retailer(request):
    if request.method == 'GET':
        return render(request,'auth/register_retailer.html',{})
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
        email = data.get('Email')
        password = data.get('Password')
        gst_number = data.get('gst number')

        collected_data = {
            "first_name":first_name,
            "last_name":last_name,
            "mobile":mobile,
            "address":address,
            "state":state,
            "city":city,
            "pincode":pincode,
            "email":email,
            "password":password,
            "gst_number":gst_number,
        }
        flag = False
        obj = Distributor.objects.filter(email=email)

        flag = flag or bool(obj.first()!=None)
        obj = Retailer.objects.filter(email=email)
        flag = flag or bool(obj.first()!=None)
        obj = Company.objects.filter(email=email)
        flag = flag or bool(obj.first()!=None)
        if not flag:
            try:
                retailer = Retailer.objects.create_retailer(email,mobile,address,state,
                                                                city,pincode,first_name,last_name,password,
                                                                gst_number=gst_number)
                if retailer is not None:
                    return redirect('mainApp:login')
            except IntegrityError as e:  
                messages={}    
                print(str(e))
                if str(e)=="UNIQUE constraint failed: mainApp_address.address":
                    messages["address"] = "Address must be unique"
                elif str(e)=="UNIQUE constraint failed: mainApp_city.city":
                    messages["city"] = "One city cannot determine multiple states"   
                elif str(e)=="UNIQUE constraint failed: mainApp_pincode.pincode":
                    messages["pincode"] = "Pincode cannot determine multiple cities"             
                else:
                    messages["gst"] = "GST number should be unique"          
                return render(request,'auth/register_retailer.html',{
                    "messages":messages,
                    "data": collected_data                    
                })
        else:
            messages = {}
            messages['email'] = "This email is already taken"
            return render(request,'auth/register_retailer.html',{
                "messages":messages,
                "data":collected_data,
                }
            )

@notAuthenticated
def register_company(request):    
    if request.method == 'GET':
        return render(request,'auth/register_company.html',{})
    else:
        data = request.POST
        print(data)
        company_name = data.get('company name')
        mobile = data.get('Mobile')
        address = data.get('address')
        state = data.get('state')
        city = data.get('city')
        pincode = data.get('pincode')
        email = data.get('Email')
        password = data.get('Password')
        gst_number = data.get('gst number')

        collected_data = {
            "company_name":company_name,            
            "mobile":mobile,
            "address":address,
            "state":state,
            "city":city,
            "pincode":pincode,
            "email":email,
            "password":password,
            "gst_number":gst_number,
        }

        
        o = Company.objects.filter(company_name=company_name)
        e = Company.objects.filter(email=email)
        flag = False
        obj = Distributor.objects.filter(email=email)

        flag = flag or bool(obj.first()!=None)
        obj = Retailer.objects.filter(email=email)
        flag = flag or bool(obj.first()!=None)
        obj = Company.objects.filter(email=email)
        flag = flag or bool(obj.first()!=None)
        
        if o.first()==None and not flag:
            print("Inside if")
            try:
                company = Company.objects.create_company(email,company_name,mobile,address,
                                                            state,city,pincode,password,gst_number=gst_number)
                if company is not None:
                    return redirect('mainApp:login')
            except IntegrityError as e:
                messages={}
                print(e,type(e),str(e))
                if str(e)=="UNIQUE constraint failed: mainApp_company.address":
                    
                    return render(request,'auth/register_company.html',{
                        "messages":{
                            "address":"Address must be unique"
                        },
                        "data":collected_data
                    })
                elif str(e)=="UNIQUE constraint failed: mainApp_city.city":
                    messages["city"] = "One city cannot determine multiple states"
                elif str(e)=="UNIQUE constraint failed: mainApp_pincode.pincode":
                    messages["pincode"] = "Pincode cannot determine multiple cities"
                elif str(e)=="UNIQUE constraint failed: mainApp_city.city":
                    messages["city"] = "City cannot determine multiple states"
                elif str(e)=="UNIQUE constraint failed: mainApp_address.address":
                    messages["address"] = "Address must be unique. Already taken"
                
                return render(request,'auth/register_company.html',{
                    "messages":messages,
                    "data":collected_data
                })

        else:
            messages = {}
            if e:
                messages['email']='The email has a;ready been taken'
            if o:
                messages['company'] = 'There is already a company with that name'
            print(messages)
            return render(request,'auth/register_company.html',{"messages":messages,"data":collected_data})

@notAuthenticated
def register_distributor(request):    
    if request.method == 'GET':
        return render(request,'auth/register_distributor.html',{})
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
        email = data.get('Email')
        password = data.get('Password')
        gst_number = data.get('gst number')
        collected_data = {
            "first_name":first_name,
            "last_name":last_name,
            "mobile":mobile,
            "address":address,
            "state":state,
            "city":city,
            "pincode":pincode,
            "email":email,
            "password":password,
            "gst_number":gst_number,
        }

        flag = False
        obj = Distributor.objects.filter(email=email)

        flag = flag or bool(obj.first()!=None)
        obj = Retailer.objects.filter(email=email)
        flag = flag or bool(obj.first()!=None)
        obj = Company.objects.filter(email=email)
        flag = flag or bool(obj.first()!=None)
       

        print("Flag",flag)
        if not flag:
            try:
                distributor = Distributor.objects.create_distributor(email,mobile,address,state,
                                                                city,pincode,first_name,last_name,password,gst_number=gst_number)

                if distributor is not None:
                    return redirect('mainApp:login')
            except IntegrityError as e:
                print(str(e))
                messages = {}
                if str(e)=="UNIQUE constraint failed: mainApp_distributor.address":
                    messages["address"] = "Address must be unique"
                elif str(e)=="UNIQUE constraint failed: mainApp_city.city":
                    messages["city"] = "One city cannot determine multiple states"
                elif str(e)=="UNIQUE constraint failed: mainApp_pincode.pincode":
                    messages["pincode"] = "Pincode cannot determine multiple cities"
                else:
                    messages["gst"] = "GST number should be unique"
                return render(request,'auth/register_distributor.html',{
                    "messages":messages,
                    "data":collected_data
                })
        else:
            messages={}
            messages['email'] = "This email has been taken"
            return render(request,'auth/register_distributor.html',{
                "messages":messages,
                "data":collected_data,
            })


def register_success(request):
    return HttpResponse("<h1> Register Success!! </h1>")

@notAuthenticated
def login_user(request):

    if request.method=='POST':
        collected_data = request.POST
        email = collected_data.get('email')
        password = collected_data.get("password")
        t = collected_data.get('type')

        user = CustomBackend.authenticate(None,request,email,password,t)
        

        if user is not None:
            request.session['user'] = user.email
            request.session['id'] = user.id
            request.session['type'] = t
            if t=='company':
                request.session['company_name'] = user.company_name
                return redirect("company:company_product_list",company_name=user.company_name)
            elif t=='distributor':
                return redirect("distributor:distributor_retailers",distributor_id=user.id)
            else:
                return redirect("retailer:retailer_distributors",retailer_id=user.id)
            print(user.email)
            return HttpResponse('<h1>Login success</h1>')
        else:
            messages={}
            messages['email'] = "No such email id was found. Register if you haven't registered yet"
            return render(request,'auth/login.html',{"messages":messages,"data":collected_data})
    else:
        return render(request,'auth/login.html',{})


def logout_user(request):
    del request.session['user']
    del request.session['id'] 
    if request.session['type']=="Company":
        del request.session['company_name']
    del request.session['type']

    return redirect('mainApp:index')


def test_page(request):
    from mainApp.models import Company1
    c = Company1.objects.filter(id=2)
    return HttpResponse("success")

