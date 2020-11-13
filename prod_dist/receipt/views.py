from django.shortcuts import render, HttpResponse

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
        return render(request,'receipt/create_receipt.html',{})

def receipt_list(request):
    return render(request,'receipt/receipt_list.html',{})

def receipt_detail(request):
    return render(request,'receipt/receipt_detail.html',{})

def receipt_product_detail(request):
    return render(request,'receipt/receipt_product_detail.html',{})