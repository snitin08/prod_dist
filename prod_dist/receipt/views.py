from django.shortcuts import render, HttpResponse

from mainApp.models import Retailer, Distributor, Company, CompanyProducts
# Create your views here.
def create_receipt(request):
    import json.decoder
    if request.method=='POST':
        arr = request.POST.get('arr')
        dict_ = json.loads(arr)
        print(dict_)
        response = {'status': 1, 'message': "Ok"} # for ok
        return HttpResponse(json.dumps(response), content_type='application/json')
        
    else:
        
        print(request.session['type'])
        if request.session['type']=='company':
            email = request.session['user']
            company = Company.objects.get(email=email)
            company_id = Company.objects.get(email=email).id
            products = CompanyProducts.objects.filter(product_company=company_id)
            extend_page="company/company_base.html"
            users = company.company_distributors.all()
            print(users)
            print(products)
        elif request.session['type']=='distributor':
            email = request.session['user']
            distributor = Distributor.objects.get(email=email)
            companies = distributor.company_set.all()
            products = CompanyProducts.objects.filter(product_company__in=companies)
            users = distributor.distributor_retailers.all()
            print(products)
            extend_page="distributor/distributor_base.html"
        else:
            return render(request,'general/404.html',{})
        return render(request,'receipt/create_receipt.html',{
            "products":products,
            "extend_page":extend_page,
            "users":users,
        })

def request_receipt(request):
    if request.method=='GET':
        if request.session['type']=='distributor':
            distributor = Distributor.objects.get(id=int(request.session['id']))
            users = distributor.company_set.all()
            products = CompanyProducts.objects.filter(product_company__in=users)
            extend_page = 'company/company_base.html'
        elif request.session['type']=='retailer':
            extend_page = 'distributor/distributor_base.html'
            retailer = Retailer.objects.get(id = int(request.session['id']))
            users = retailer.distributor_set.all()
            companies = set()
            for user in users:
                company = user.company_set.all()
                for c in company:
                    companies.add(c.id)
            print(companies)
            products = CompanyProducts.objects.filter(product_company__in=companies)
            print(products)
        return render(request,'receipt/request_receipt.html',
        {
            "extend_page":extend_page,
            "users":users,
            "products":products
        })


def receipt_list(request):
    return render(request,'receipt/receipt_list.html',{})

def receipt_detail(request):
    return render(request,'receipt/receipt_detail.html',{})

def receipt_product_detail(request):
    return render(request,'receipt/receipt_product_detail.html',{})
