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
            company_id = Company.objects.get(email=email).id
            products = CompanyProducts.objects.filter(product_company=company_id)
            print(products)
        elif request.session['type']=='distributor':
            email = request.session['user']
            distributor = Distributor.objects.get(email=email)
            companies = distributor.company_set.all()
            products = CompanyProducts.objects.filter(product_company__in=companies)
            print(products)
        return render(request,'receipt/create_receipt.html',{
            "products":products
        })

def receipt_list(request):
    return render(request,'receipt/receipt_list.html',{})

def receipt_detail(request):
    return render(request,'receipt/receipt_detail.html',{})

def receipt_product_detail(request):
    return render(request,'receipt/receipt_product_detail.html',{})
