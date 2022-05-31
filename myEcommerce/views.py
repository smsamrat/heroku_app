

from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse


# Create your views here.

def index(request):
    return HttpResponseRedirect(reverse('store'))
