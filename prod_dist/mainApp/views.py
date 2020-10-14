from django.shortcuts import render, HttpResponse

# Create your views here.
def register_retailer(request):
    if request.method == 'GET':
        return render(request,'auth/register_retailer.html',{})
    
def register_success(request):
    return HttpResponse("<h1> Register Success!! </h1>")