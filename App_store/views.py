import imp
from urllib import request
from django.shortcuts import redirect, render
from django.views.generic import ListView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

# Models
from .models import Category, Product

# Create your views here.

def store(request):
    products = Product.objects.all()
    paginator = Paginator(products, 8,orphans = 1)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'app_store/store.html', { 'object_list': page_obj,'page_number':int(page_number),'paginator':paginator })


def product_fetch_by_category(request, slug):
    if(Category.objects.filter(slug=slug)):
        products = Product.objects.filter(category__slug=slug)
        return render(request,'app_store/store.html',context={'object_list':products})
    else:
        messages.warning(request,'Product is not available')
        return redirect('store')

def product_details(request,cat_slug,prod_slug):
    if(Category.objects.filter(slug=cat_slug)):
        if(Product.objects.filter(slug=prod_slug)):
            products = Product.objects.filter(slug=prod_slug).first()
    return render(request,'app_store/details_page.html',context={'single_product':products})

def SearchProduct(request):
    search = request.GET['search_item']
    products = Product.objects.filter(name__icontains=search).order_by('-name')
    if products !=None and products !='':
        return render(request,'app_store/search.html',context={'object_list':products})
    else:
        messages.warning(request,'Product Not Found')
        return redirect('store')
        
        