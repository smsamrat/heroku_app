
from django import template
from App_order.models import Order
from django.shortcuts import render
register = template.Library()
  
@register.filter
def cart_total(user):
   order = Order.objects.filter(user=user, orderd=False)
   if order.exists():
       return order[0].orderItems.count()
   else:
       return 0 
