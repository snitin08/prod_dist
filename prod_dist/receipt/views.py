from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
import json
from mongoengine.queryset.visitor import Q
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
def approve_purchase_order(receipt_id,session):
    pass

def request_receipt(request):
    if request.method=='GET':
        if request.session['type']=='company':
            return render(request,'general/404.html',{})
        elif request.session['type']=='distributor':
            distributor = Distributor.objects.get(id=int(request.session['id']))
            users = distributor.company_set.all()
            if users:
                return redirect('receipt:company_products',company_id=users[0].id)
            else:
                return HttpResponse("<h1>There are no companies</h1>")
        elif request.session['type']=='retailer':            
            retailer = Retailer.objects.get(id = int(request.session['id']))
            users = retailer.distributor_set.all()
            if users:
                return redirect('receipt:distributor_products',distributor_id=users[0].id)
            else:
                return HttpResponse("<h1>There are no distributors</h1>")
    


def search(data,session):
    year = int(data.get('year') or '0')
    month = int(data.get('month') or '0')
    day = int(data.get('day') or '0')
    search_type = data.get('search_type')

    if search_type=='sent_receipts':
        query = Q(requested=False) & Q(from_id=int(session['id'])) & Q(from_type=session['type'])
        if year!=0:
            query = query & Q(year=year)
        if month!=0:
            query = query & Q(month=month)
        if day!=0:
            query = query & Q(day=day)
        sent_receipts = Receipt.objects(query)
        received_receipts = Receipt.objects(Q(requested=False) & Q(to_id=int(session['id'])) & Q(to_type=session['type']))
        sent_requests = Receipt.objects(Q(requested=True) & Q(to_id=int(session['id'])) & Q(to_type=session['type']))
        received_requests = Receipt.objects(Q(requested=True) & Q(from_id=int(session['id'])) & Q(from_type=session['type']))
        return {
            "sent_receipts":sent_receipts,
            "received_receipts":received_receipts,
            "sent_requests":sent_requests,
            "received_requests":received_requests,
        }
    elif search_type=='received_receipts':
        query = Q(requested=False) & Q(to_id=int(session['id'])) & Q(to_type=session['type'])
        if year!=0:
            query = query & Q(year=year)
        if month!=0:
            query = query & Q(month=month)
        if day!=0:
            query = query & Q(day=day)
        sent_receipts = Receipt.objects(Q(requested=False) & Q(from_id=int(session['id'])) & Q(from_type=session['type']))
        received_receipts = Receipt.objects(query)
        sent_requests = Receipt.objects(Q(requested=True) & Q(to_id=int(session['id'])) & Q(to_type=session['type']))
        received_requests = Receipt.objects(Q(requested=True) & Q(from_id=int(session['id'])) & Q(from_type=session['type']))
        return {
            "sent_receipts":sent_receipts,
            "received_receipts":received_receipts,
            "sent_requests":sent_requests,
            "received_requests":received_requests,
        }

    elif search_type=='sent_requests':
        query = Q(requested=True) & Q(to_id=int(session['id'])) & Q(to_type=session['type'])
        if year!=0:
            query = query & Q(year=year)
        if month!=0:
            query = query & Q(month=month)
        if day!=0:
            query = query & Q(day=day)
        sent_receipts = Receipt.objects(Q(requested=False) & Q(from_id=int(session['id'])) & Q(from_type=session['type']))
        received_receipts = Receipt.objects(Q(requested=False) & Q(to_id=int(session['id'])) & Q(to_type=session['type']))
        sent_requests = Receipt.objects(query)
        received_requests = Receipt.objects(Q(requested=True) & Q(from_id=int(session['id'])) & Q(from_type=session['type']))
        return {
            "sent_receipts":sent_receipts,
            "received_receipts":received_receipts,
            "sent_requests":sent_requests,
            "received_requests":received_requests,
        }
    else:
        query = Q(requested=True) & Q(from_id=int(session['id'])) & Q(from_type=session['type'])
        if year!=0:
            query = query & Q(year=year)
        if month!=0:
            query = query & Q(month=month)
        if day!=0:
            query = query & Q(day=day)
        sent_receipts = Receipt.objects(Q(requested=False) & Q(from_id=int(session['id'])) & Q(from_type=session['type']))
        received_receipts = Receipt.objects(Q(requested=False) & Q(to_id=int(session['id'])) & Q(to_type=session['type']))
        sent_requests = Receipt.objects(Q(requested=True) & Q(to_id=int(session['id'])) & Q(to_type=session['type']))
        received_requests = Receipt.objects(query)
        return {
            "sent_receipts":sent_receipts,
            "received_receipts":received_receipts,
            "sent_requests":sent_requests,
            "received_requests":received_requests,
        }
    

def receipt_list(request):
    if request.method=='GET':
        data = request.GET.dict()
        print(data)
        
        if request.session['type']=='company':
            extend_page = 'company/company_base.html'
        elif request.session['type']=='distributor':
            extend_page = 'distributor/distributor_base.html'
        else:
            extend_page = 'retailer/retailer_base.html'
        
        search_result = search(data,request.session)
        print(search_result)
        
        sent_receipts = search_result['sent_receipts']
        received_receipts = search_result['received_receipts']
        sent_requests = search_result['sent_requests']
        received_requests = search_result['received_requests']

        return render(request,'receipt/receipt_list.html',{
            "extend_page":extend_page,
            "sent_receipts":sent_receipts,
            "received_receipts":received_receipts,
            "sent_requests":sent_requests,
            "received_requests":received_requests,
        })

def receipt_detail(request,receipt_id):
    if request.session['type']=='company':
        extend_page = 'company/company_base.html'
    elif request.session['type']=='distributor':
        extend_page = 'distributor/distributor_base.html'
    else:
        extend_page = 'retailer/retailer_base.html'
    if request.method=='GET':
        
        receipt = Receipt.objects(id=receipt_id).first()
        user_id = int(request.session['id'])
        user_type = request.session['type']
        saisfy = (receipt.from_id==user_id and receipt.from_type==user_type) or (receipt.to_id==user_id and receipt.to_type==user_type)
        if saisfy:
            print(receipt)
            return render(request,'receipt/receipt_detail.html',{
                "extend_page":extend_page,
                "receipt":receipt,
            })
        else:
            return render(request,"general/404.html",{})
    else:
        data = request.POST.dict()
        receipt = Receipt.objects(id=receipt_id).first()
        if data.get("post_type")=="approve":
            
            user_id = int(request.session['id'])
            user_type = request.session['type']
            satisfy = (receipt.from_id==user_id and receipt.from_type==user_type) or (receipt.to_id==user_id and receipt.to_type==user_type)
            if satisfy:
                receipt.modify(requested=False)
                return redirect('receipt:receipt_list')
        else:
            print(data)
            defects = eval(data['defects'])
            comments = data['comments']
            defective = False
            products = receipt.products
            for i in range(len(defects)):
                n = int(defects[i])
                if n>=1:
                    defective = True
                    receipt.products[i].defective = n
            receipt.comments = comments
            receipt.defective = defective
            receipt.save()            
            response = {'status': 1, 'message': "Ok"} # for ok
            return HttpResponse(json.dumps(response), content_type='application/json')


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
    if request.method=='GET':
        if request.session.get('type')=='retailer':
            retailer = Retailer.objects.get(id=int(request.session.get('id')))
            
            distributors = set([k['id'] for k in retailer.distributor_set.all().values('id')])
            print(distributors)
            if distributor_id in distributors:
                distributor = Distributor.objects.get(id=distributor_id)
                companies = distributor.company_set.all()
                products = CompanyProducts.objects.filter(product_company_id__in=companies)
                print(products)
                # products = list(products.values())
                # json.dumps(products)
                users = retailer.distributor_set.all()
                extend_page = 'retailer/retailer_base.html'
                print(distributor_id)
                return render(request,'receipt/distributor_products.html',{
                    "products":products,
                    "users":users,
                    "extend_page":extend_page,
                    "selected_id":distributor_id,
                })
            else:
                return render(request,"general/404.html",{})
        else:
            return render(request,"general/404.html",{})
    else:
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']
        print(data)
        distributor = Distributor.objects.get(id=distributor_id)
        retailer = Retailer.objects.get(id=int(request.session['id']))
        arr = data.get('arr')
        arr = eval(arr)
        products = arr.get('products')
        user_to = arr.get('user_to')
        sub_total = arr.get('subtotal')
        taxes = arr.get('total_tax')
        total = arr.get('total_price')
        discount = arr.get('total_discount')

        from_id = distributor_id
        to_id = request.session['id']
        from_type = "distributor"
        to_type = "retailer"
        from_name = distributor.first_name+" "+distributor.last_name
        to_name = retailer.first_name+" "+retailer.last_name
        from_address = distributor.address
        to_address = retailer.address
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
                
        requested = True
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
            total=total,
            requested=requested
        )
        r.save()

        response = {'status': 1, 'message': "Ok"} # for ok
        return HttpResponse(json.dumps(response), content_type='application/json')

def company_products(request,company_id):
    if request.method=='GET':
        if request.session["type"]=='distributor':
            distributor = Distributor.objects.filter(id=int(request.session['id'])).first()
            companies = set([k['id'] for k in distributor.company_set.all().values('id')])
            print(companies)
            if company_id in companies:
                products = CompanyProducts.objects.filter(product_company_id=company_id)
                extend_page = "distributor/distributor_base.html"
                users = distributor.company_set.all()
                selected_id = company_id
                if products:
                    return render(request,'receipt/distributor_products.html',{
                    "products":products,
                    "users":users,
                    "extend_page":extend_page,
                    "selected_id":selected_id,
                    })
                else:
                    return render(request,'receipt/access_denied.html',{"extend_page":extend_page})
            else:
                return render(request,'general/404.html',{})
        else:
            return render(request,"general/404.html",{})
    else:
        data = request.POST.dict()
        company = Company.objects.get(id=company_id)
        distributor = Distributor.objects.get(id=int(request.session['id']))
        del data['csrfmiddlewaretoken']
        print(data)
        arr = data.get('arr')
        arr = eval(arr)
        products = arr.get('products')
        user_to = arr.get('user_to')
        sub_total = arr.get('subtotal')
        taxes = arr.get('total_tax')
        discount = arr.get('total_discount')
        total = arr.get('total_price')

        from_id = company_id
        to_id = request.session['id']
        from_type = "company"
        to_type = "distributor"
        from_name = company.company_name
        to_name = distributor.first_name+" "+distributor.last_name
        from_address = company.address
        to_address = distributor.address
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
                
        requested = True
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
            total=total,
            requested=requested
        )
        r.save()

        response = {'status': 1, 'message': "Ok"} # for ok
        return HttpResponse(json.dumps(response), content_type='application/json')
        


def receipt_stats(request):
    return render(request,'receipt/receipt_stats.html',{
        "extend_page":"company/company_base.html"
    })

def access_denied(request):
    if request.session['type']=='retailer':
        extend_page = 'retailer/retailer_base.html'
    elif request.session['type']=='distributor':
        extend_page = 'distributor/distributor_base.html'
    else:
        extend_page = 'comapny/comapny_base.html'
    return render(request,'receipt/access_denied.html',{"extend_page":extend_page})

