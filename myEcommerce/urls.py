
from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('App_account.urls')),
    path('store/', include('App_store.urls')),
    path('order/', include('App_order.urls')),
    path('payment/', include('App_payment.urls')),
    path('', views.index,name ='index'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
