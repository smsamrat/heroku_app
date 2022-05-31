

from django.contrib import admin
from App_store.models import Category,Product

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields ={'slug':('name',)}
    # list_display =('product_name','stoke','price','create_date','category','is_available')

admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
