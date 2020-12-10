from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
import json
from mainApp.models import Retailer, Distributor, Company, CompanyProducts
from receipt.models import Products,Receipt
# Create your views here.
def create_receipt(request):
    import json.decoder
    if request.method=='POST':
        arr = request.POST.get('arr')
        dict_ = json.loads(arr)
        print(dict_)
        products = dict_['products']
        from_type = request.session['type']
        user_to = int(dict_['user_to'])
        if request.session['type']=='company':
            from_model = Company.objects.get(
                id=int(request.session['id'])
            )
            to_model = Distributor.objects.get(id=user_to)
            from_name = from_model.company_name
            to_type = 'distributor'
            to_name = to_model.first_name+" "+to_model.last_name
            
        else:
            from_model = Distributor.objects.get(
                id=int(request.session['id'])
            )
            to_model = Retailer
            from_name = from_model.first_name+" "+from_model.last_name
            to_type = 'retailer'
            to_model = Retailer.objects.get(id=user_to)
            to_name = to_model.first_name+" "+to_model.last_name

        
        to_id = int(dict_['user_to'])
        from_address = from_model.address
        to_address = to_model.address
        from_id = request.session['id']
        sub_total = dict_['subtotal']
        taxes = dict_['total_tax']
        total = dict_['total_price']
        discount = dict_['total_discount']
        
        products_list = []
        for product in products:
            p = Products(
                prod_name=product['product'],
                price = float(product['product_price']),
                tax = float(product['product_tax']),
                discount = float(product['product_discount']),
                quantity = int(product['product_quantity'])
            )
            products_list.append(p)
        r = Receipt(
            from_id=from_id,
            to_id=to_id,
            from_type=from_type,
            to_type=to_type,
            from_name=from_name,
            to_name=to_name,
            from_address=from_address,
            to_address=to_address,
            products=products_list,
            sub_total=sub_total,
            taxes=taxes,
            discount=discount,
            total=total
        )
        r.save()
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
    if request.session['type']=='company':
        extend_page = 'company/company_base.html'
    elif request.session['type']=='distributor':
        extend_page = 'distributor/distributor_base.html'
    else:
        extend_page = 'retailer/retailer_base.html'
    return render(request,'receipt/receipt_list.html',{
        "extend_page":extend_page,
    })

def receipt_detail(request):
    if request.session['type']=='company':
        extend_page = 'company/company_base.html'
    elif request.session['type']=='distributor':
        extend_page = 'distributor/distributor_base.html'
    else:
        extend_page = 'retailer/retailer_base.html'
    return render(request,'receipt/receipt_detail.html',{
        "extend_page":extend_page,
    })

def receipt_product_detail(request):
    if request.session['type']=='company':
        extend_page = 'company/company_base.html'
    elif request.session['type']=='distributor':
        extend_page = 'distributor/distributor_base.html'
    else:
        extend_page = 'retailer/retailer_base.html'
    return render(request,'receipt/receipt_product_detail.html',{
        "extend_page":extend_page,
    })

"""
JSON returning functions for ajax requests
"""
def distributor_products(request,distributor_id):
    if request.session.get('type')=='retailer':
        retailer = Retailer.objects.get(id=int(request.session.get('id')))
        
        distributors = set([k['id'] for k in retailer.distributor_set.all().values('id')])
        print(distributors)
        if distributor_id in distributors:
            distributor = Distributor.objects.get(id=distributor_id)
            companies = distributor.company_set.all()
            products = CompanyProducts.objects.filter(product_company_id__in=companies)
            products = list(products.values())
            json.dumps(products)
            return JsonResponse(products, safe=False)
        else:
            return HttpResponse({"Access denied":-1}, content_type='application/json')
    else:
        return HttpResponse({"Access denied":-1}, content_type='application/json')
