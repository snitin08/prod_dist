from django.shortcuts import render, HttpResponse, redirect

# Create your views here.
def index(request):
    if request.session.get('UID')==None:
        return render(request,'auth/register.html',{})

def register_retailer(request):
    if request.method == 'GET':
        return render(request,'auth/register_retailer.html',{})
    else:
        data = request.POST
        print(data)
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

        return redirect('mainApp:register_success')

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

        return redirect('mainApp:register_success')

def register_distributor(request):
    if request.method == 'GET':
        return render(request,'auth/register_distributor.html',{})
    else:
        data = request.POST
        print(data)
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
        return redirect('mainApp:register_success')
    
def register_success(request):
    return HttpResponse("<h1> Register Success!! </h1>")