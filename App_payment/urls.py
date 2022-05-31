
from django.urls import path
from . import views


urlpatterns = [
   path('checkout/',views.checkout, name="checkout"),
   path('pay/',views.payment, name="payment"),
   path('status/',views.complete, name="complete"),
   path('purchase-item/<tran_id>/<val_id>/',views.purchase, name="purchase"),
]
