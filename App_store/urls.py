
from django.contrib import admin
from django.urls import path
from App_store import views

urlpatterns = [
    path('', views.store, name='store'),
    path('search/', views.SearchProduct, name='SearchProduct'),
    path('details/<str:cat_slug>/<str:prod_slug>/', views.product_details, name='product_details'),
    path('cetegory/<str:slug>/',views.product_fetch_by_category, name='category')
]
