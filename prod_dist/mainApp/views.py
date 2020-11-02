from django.shortcuts import render, HttpResponse, redirect
from .models import Company,Distributor,Retailer
from .models import CustomBackend
from django.contrib.auth import login,logout

# Create your views here.
def index(request):
    if request.session.get('UID')==None:
        print(request.session.get('user'))
        return render(request,'auth/register.html',{})

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
        }
        obj = Retailer.objects.filter(email=email)
        if obj.first()==None:
            retailer = Retailer.objects.create_retailer(email,mobile,address,state,
                                                            city,pincode,first_name,last_name,password)
            if retailer is not None:
                return redirect('mainApp:register_success')
            else:
                return render(request,'auth/register_retailer.html',{})
        else:
            messages = {}
            messages['email'] = "This email is already taken"
            return render(request,'auth/register_retailer.html',{
                "messages":messages,
                "data":collected_data,
                }
            )

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

        collected_data = {
            "company_name":company_name,            
            "mobile":mobile,
            "address":address,
            "state":state,
            "city":city,
            "pincode":pincode,
            "email":email,
            "password":password,
        }

        
        o = Company.objects.filter(company_name=company_name)
        e = Company.objects.filter(email=email)
        
        if o.first()==None and e.first()==None:
            print("Inside if")
            company = Company.objects.create_company(email,company_name,mobile,address,
                                                        state,city,pincode,password)
            if company is not None:
                return redirect('mainApp:register_success')
            else:
                return render(request,'auth/register_company.html',{})
        else:
            messages = {}
            if e:
                messages['email']='The email has a;ready been taken'
            if o:
                messages['company'] = 'There is already a company with that name'
            print(messages)
            return render(request,'auth/register_company.html',{"messages":messages,"data":collected_data})
        


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
        }

        obj = Distributor.objects.filter(email=email)

        if obj.first()==None:
            distributor = Distributor.objects.create_distributor(email,mobile,address,state,
                                                            city,pincode,first_name,last_name,password)

            if distributor is not None:
                return redirect('mainApp:register_success')
            else:
                return render(request,'auth/register_distributor.html',{})
        else:
            messages={}
            messages['email'] = "This email has been taken"
            return render(request,'auth/register_distributor.html',{
                "messages":messages,
                "data":collected_data,
            })
    
def register_success(request):
    return HttpResponse("<h1> Register Success!! </h1>")

def login_user(request):

    if request.method=='POST':
        collected_data = request.POST
        email = collected_data.get('email')
        password = collected_data.get("password")
        t = collected_data.get('type')

        user = CustomBackend.authenticate(None,request,email,password,t)
        

        if user is not None:
            request.session['user'] = user.email
            print(user.email)
            return redirect('mainApp:register_success')
        else:
            messages={}
            messages['email'] = "No such email id was found. Register if you haven't registered yet"
            return render(request,'auth/login.html',{"messages":messages,"data":collected_data})
    else:
        return render(request,'auth/login.html',{})


def logout_user(request):
    del request.session['user']
    return redirect('mainApp:index')


