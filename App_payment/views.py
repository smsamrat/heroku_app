from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from App_order.models import Order,Cart
from App_account.models import Profile
from .models import BillignsAddress
from .forms import BillignsAddressForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
#payment
import requests
from sslcommerz_python.payment import SSLCSession
from decimal import Decimal
import socket

# Create your views here.
@login_required
def checkout(request):
    save_address = BillignsAddress.objects.get_or_create(user=request.user)[0]

    form = BillignsAddressForm(instance=save_address)
    if request.method == 'POST':
        form = BillignsAddressForm(request.POST,instance=save_address)
        if form.is_valid():
            form.save()
            form = BillignsAddressForm(instance=save_address)
    # order_item = Cart.objects.filter(user=request.user, purchased=False)#aivbae dia jai
    order_qs = Order.objects.filter(user=request.user, orderd=False)
    order_item = order_qs[0].orderItems.all()
    order_total = order_qs[0].get_totals

    return render(request,'app_payment/checkout.html',context={'form':form,'order_item':order_item,
    'order_total':order_total,
    'save_address':save_address
    
    })

def payment(request):
    save_address = BillignsAddress.objects.get_or_create(user = request.user)
    save_address = save_address[0]
    if not save_address.is_fully_filled():
        messages.warning(request,'Please save the delivary address')
        return redirect('checkout')
        
    if not request.user.profile.is_fully_filled():
        messages.info(request,'Please Fill up your Profile')
        return redirect('custom_profile')

    store_id = 'abc626e225657a3c'
    API_key = 'abc626e225657a3c@ssl'
    mypayment = SSLCSession(sslc_is_sandbox=True, sslc_store_id=store_id, sslc_store_pass=API_key)

    status_url = request.build_absolute_uri(reverse('complete'))
    # print(status_url)
    mypayment.set_urls(success_url=status_url, fail_url=status_url, cancel_url=status_url, ipn_url=status_url)


    order_qs = Order.objects.filter(user= request.user, orderd = False)
    order_items = order_qs[0].orderItems.all()
    order_items_count = order_qs[0].orderItems.count()
    order_total = order_qs[0].get_totals()

    mypayment.set_product_integration(total_amount=Decimal(order_total), currency='BDT', product_category='Mixed', product_name=order_items, num_of_item=order_items_count, shipping_method='Courier', product_profile='None')

    current_user = request.user

    mypayment.set_customer_info(name=current_user.profile.full_name, email=current_user.email, address1=current_user.profile.address_1, address2=current_user.profile.address_1, city=current_user.profile.city, postcode=current_user.profile.zipcode, country=current_user.profile.country, phone=current_user.profile.phone)

    mypayment.set_shipping_info(shipping_to=current_user.profile.full_name, address=save_address.address, city=save_address.city, postcode=save_address.zipcode, country=save_address.country)

    response_data = mypayment.init_payment()
    # print(response_data)

    return redirect(response_data['GatewayPageURL'])

@csrf_exempt
def complete(request):
    if request.method =='POST' or request.method =='post':
        payment_data = request.POST
        status = payment_data['status']
        
        if status == 'VALID':
            tran_id = payment_data['tran_id']
            val_id = payment_data['val_id']
            messages.success(request,f"Payment Is Successfully!")
            return HttpResponseRedirect(reverse('purchase', kwargs={'tran_id':tran_id,'val_id':val_id}))
        elif status == 'FAILED':
            messages.warning(request,f"Payment Failed ! Please Try Again After! 5 second Home Page will be redirected")
        elif status == 'CANCEL':
            messages.warning(request,f"Payment Cancel ! After 5 second Home Page will be redirected")

    return render(request,"app_payment/complete.html",context={})

def purchase (request, tran_id, val_id):
    order_qs = Order.objects.filter(user = request.user, orderd = False)
    order = order_qs[0]
    orderId = tran_id
    order.orderd = True
    order.orderId = orderId
    order.paymentId = val_id
    order.save()
    cart_items = Cart.objects.filter(user = request.user, purchased = False)
    for item in cart_items:
        item.purchased = True
        item.save()
    return HttpResponseRedirect(reverse('store'))
