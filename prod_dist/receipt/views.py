from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
import json
import pytesseract
pytesseract.pytesseract.tesseract_cmd = "E:\\Downloads\\Tesseract OCR\\tesseract.exe"

import subprocess
from .table_detect import table_detect, colfilter, get_text, get_annotations_xlsx, find_table, find_below_table

from numpy.core.numeric import normalize_axis_tuple
from mongoengine.queryset.visitor import Q
from mainApp.models import Retailer, Distributor, Company, CompanyProducts
from receipt.models import Products,Receipt
from pdf2image import convert_from_path,convert_from_bytes
import base64
from prod_dist.settings import BASE_DIR
import pytesseract
from pytesseract import Output
import numpy as np
import cv2
from django.urls import reverse

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Create your views here.
def create_receipt(request):
    import json.decoder
    if request.method=='POST':
        arr = request.POST.get('arr')
        print(arr)
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
        if products:
            return render(request,'receipt/create_receipt.html',{
                "products":products,
                "extend_page":extend_page,
                "users":users,
            })
        else:
            return render(request,"receipt/access_denied.html",{
                "extend_page":extend_page
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
                return render(request,"receipt/access_denied.html",{
                    "extend_page":"distributor/distributor_base.html"
                })
        elif request.session['type']=='retailer':            
            retailer = Retailer.objects.get(id = int(request.session['id']))
            users = retailer.distributor_set.all()
            if users:
                return redirect('receipt:distributor_products',distributor_id=users[0].id)
            else:
                return render(request,"receipt/access_denied.html",{
                    "extend_page":"retailer/retailer_base.html"
                })
    


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
        if receipt:
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
                if products:
                    return render(request,'receipt/distributor_products.html',{
                        "products":products,
                        "users":users,
                        "extend_page":extend_page,
                        "selected_id":distributor_id,
                    })
                else:
                    return render(request,"receipt/access_denied.html",{
                        "extend_page":extend_page
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
        extend_page = 'company/company_base.html'
    return render(request,'receipt/access_denied.html',{"extend_page":extend_page})

def process_receipt(request):
    if request.method == 'POST':
        data = request.POST.dict()
        del data['csrfmiddlewaretoken']
        print(request.FILES)
        file1 = request.FILES['file1']
        file2 = request.FILES['file2']
        x = file1.read()
        f = open(BASE_DIR + '/media/current.pdf', 'wb')
        f.write(x)
        f.close()
        y = file2.read()
        g = open(BASE_DIR + '/media/template.csv', 'wb')
        g.write(y)
        g.close()
        annotation, table, below_table = process_invoice(BASE_DIR + '/media/current.pdf', BASE_DIR + '/media/template.csv')
        print(annotation)
        print(table)
        print(below_table)
        request.session['annotations'] = annotation
        request.session['table'] = table
        request.session['below_table'] = below_table
        return redirect('receipt:submit_receipt')
    else:
        if request.session['type']=='retailer':
            extend_page = 'retailer/retailer_base.html'
        elif request.session['type']=='distributor':
            extend_page = 'distributor/distributor_base.html'
        else:
            extend_page = 'company/company_base.html'
        return render(request, 'receipt/receipt_process.html',{"extend_page":extend_page})

def process_invoice(filename, templatename):
    images = convert_from_path(filename, 200,fmt="jpeg")
    annotate_dict = get_annotations_xlsx(templatename)
    tab_result = list()
    print(len(images))
    start_of_table = annotate_dict['page 1']['Start Of Table'][1]
    result = get_text(annotate_dict, np.copy(images[0]), 901, 1200)
    flg = False
    below_tab_result = list()
    
    for image in images:
        image.save(str(BASE_DIR)+'\\media\\page_1.jpeg', 'JPEG')  
        cmd = '"E:\Downloads\ImageMagic\ImageMagick-6.9.11-Q16-20201228T144714Z-001\ImageMagick-6.9.11-Q16\convert.exe" "E:/Nitin/RVCE/5 Sem/DBMS/Self Study Lab/prod_dist/media/page_1.jpeg" -type Grayscale -negate -define morphology:compose=darken -morphology Thinning "Rectangle:1x80+0+0<" -negate "E:/Nitin/RVCE/5 Sem/DBMS/Self Study Lab/prod_dist/media/page_1-t.jpeg"'
        print(cmd)
        subprocess.call(cmd, shell=True)
        new_img = cv2.imread(str(BASE_DIR)+'\\media\\page_1-t.jpeg')
        new_img2 = cv2.imread(str(BASE_DIR)+'\\media\\page_1.jpeg')
        new_img2 = cv2.bilateralFilter(new_img2,5,75,75)
#        print(annotate_dict)
#        print(new_img.shape[0],new_img.shape)
        rgb = np.copy(new_img)
        print("RGB",rgb.shape)
        new_crd = table_detect(rgb)
        NO_OF_COLS = annotate_dict['ncols']
        new_lst = list()
        below_table = list()
        for x in new_crd: 
            if colfilter(x,rgb,NO_OF_COLS,start_of_table) == int(NO_OF_COLS):
                new_lst.append(x)
            elif x[3] > start_of_table:
                below_table.append(x)
            else:
                pass
        tmp3 = np.copy(rgb)
        if len(new_lst)>=1:
            new_lst = new_lst[1:]
        tab_result += find_table(tmp3, new_img2, new_lst)
        if flg==False:
            below_tab_result = find_below_table(np.copy(new_img2), below_table)
            flg = True
    return result, tab_result, below_tab_result

# def submit_receipt(request):
#     if request.method == 'POST':
#         data = request.POST.dict()
#         del data['csrfmiddlewaretoken']
#         print(data)
#         from_type = request.session['type']
#         user_to = int(data['user_to'])
#         if request.session['type']=='company':
#             from_model = Company.objects.get(
#                 id=int(request.session['id'])
#             )
#             to_model = Distributor.objects.get(id=user_to)
#             from_name = from_model.company_name
#             to_type = 'distributor'
#             to_name = to_model.first_name+" "+to_model.last_name
            
#         else:
#             from_model = Distributor.objects.get(
#                 id=int(request.session['id'])
#             )
#             to_model = Retailer
#             from_name = from_model.first_name+" "+from_model.last_name
#             to_type = 'retailer'
#             to_model = Retailer.objects.get(id=user_to)
#             to_name = to_model.first_name+" "+to_model.last_name

        
#         to_id = int(data['user_to'])
#         from_address = from_model.address
#         to_address = to_model.address
#         from_id = request.session['id']
        
#         i = '1'
#         j = '1'
#         products = list()
#         while i in data:
#             j = '1'
#             product = dict()
#             while j in data:
#                 key = 'row-'+str(i)+'-'+str(j)
#                 product.update({data[j]:data[key]})
#                 j = str(int(j)+1)
#             products.append(product)
#             i = str(int(i)+1)
#         print(products)
#         products_list = list() 
#         for product in products:
#             pname = product['Product Name']
#             price = float(product['Product Price'].split('$')[1])
#             quantity = int(product['Quantity'])
#             tax = None
#             discount = None
#             if 'Taxes' in product:
#                 tax = float(product['Taxes'])
#             if 'Discount' in product:
#                 discount = float(product['Discount'])    
#             p = Products(
#                 prod_name=pname,
#                 price = price,
#                 tax = tax,
#                 discount = discount,
#                 quantity = quantity
#             )
#             products_list.append(p)
#         sub_total = data['sub-total']
#         taxes = data['taxes']
#         total = data['total']
#         discount = data['discount']
#         r = Receipt(
#             from_id=from_id,
#             to_id=to_id,
#             from_type=from_type,
#             to_type=to_type,
#             from_name=from_name,
#             to_name=to_name,
#             from_address=from_address,
#             to_address=to_address,
#             products=products_list,
#             sub_total=sub_total,
#             taxes=taxes,
#             discount=discount,
#             total=total
#         )
#         r.save()
#         return redirect('receipt:receipt_list')
#     else:
#         if request.session['type']=='company':
#             email = request.session['user']
#             company = Company.objects.get(email=email)
#             company_id = Company.objects.get(email=email).id
#             products = CompanyProducts.objects.filter(product_company=company_id)
#             extend_page="company/company_base.html"
#             users = company.company_distributors.all()
#             print(users)
#             print(products)
#         elif request.session['type']=='distributor':
#             email = request.session['user']
#             distributor = Distributor.objects.get(email=email)
#             companies = distributor.company_set.all()
#             products = CompanyProducts.objects.filter(product_company__in=companies)
#             users = distributor.distributor_retailers.all()
#             print(products)
#             extend_page="distributor/distributor_base.html"
#         else:
#             return render(request,'general/404.html',{})
#         if products:
#             annotation = request.session['annotations']
#             table = request.session['table']
#             below_table = request.session['below_table']
#             print(annotation)
#             print(table)
#             print(below_table) 
#             return render(request,'receipt/submit_receipt.html',{
#                 "extend_page":extend_page,
#                 "users":users,
#                 'annotations' : annotation,
#                 'table' : table,
#                 'below_table' : below_table
#                 })
#         else:
#             return render(request,"receipt/access_denied.html",{
#                 "extend_page":extend_page
#             })

def submit_receipt(request):
    if request.method == 'POST':
        data = request.POST
        tableHeader = data.getlist('tableHeader[]')
        tableColumn_1 = data.getlist('tableColumn-1[]')
        tableColumn_2 = data.getlist('tableColumn-2[]')
        tableColumn_3 = data.getlist('tableColumn-3[]')
        print(tableHeader)
        print(tableColumn_1,tableColumn_2,tableColumn_3)
        data = data.dict()
        del data['csrfmiddlewaretoken']
        del data['tableHeader[]']
        del data['tableColumn-1[]']
        del data['tableColumn-2[]']
        del data['tableColumn-3[]']
        print(data)
        
        # return HttpResponse("success")
        from_type = request.session['type']
        user_to = int(data['user_to'])
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

        
        to_id = int(data['user_to'])
        from_address = from_model.address
        to_address = to_model.address
        from_id = request.session['id']
        
        
        products = []
        products_list = []

        for i in range(len(tableColumn_1)):
            p = {}
            if tableHeader[0]=='quantity':
                p[tableHeader[0]] = int(tableColumn_1[i])
            elif tableHeader[0]=='price':
                p[tableHeader[0]] = float(tableColumn_1[i])
            else:
                p[tableHeader[0]] = tableColumn_2[i]
            if tableHeader[1]=='quantity':
                p[tableHeader[1]] = int(tableColumn_2[i])
            elif tableHeader[1]=='price':
                p[tableHeader[1]] = float(tableColumn_2[i])
            else:
                p[tableHeader[1]] = tableColumn_2[i]
            if tableHeader[2]=='quantity':
                p[tableHeader[2]] = int(tableColumn_3[i])
            elif tableHeader[2]=='price':
                p[tableHeader[2]] = float(tableColumn_3[i])
            else:
                p[tableHeader[2]] = tableColumn_3[i]
            p = Products(**p)
            products_list.append(p)
        sub_total = float(data['sub_total'])
        taxes = float(data['taxes'])
        total = float(data['total'])
        discount = float(data['discount'])
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
        # return HttpResponse('success')
        return redirect('receipt:receipt_list')
    else:
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
        if products and users:
            annotation = request.session['annotations']
            table = request.session['table']
            below_table = request.session['below_table']
            print(annotation)
            print(table)
            print(below_table) 
            return render(request,'receipt/submit_receipt.html',{
                "extend_page":extend_page,
                "users":users,
                'annotations' : annotation,
                'table' : table,
                'below_table' : below_table
                })
        else:
            return render(request,"receipt/access_denied.html",{
                "extend_page":extend_page
            })