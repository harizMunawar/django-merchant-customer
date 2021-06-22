from django.contrib import admin
from core.models import Merchant, Customer

@admin.register(Merchant)
class MerchantAdmin(admin.ModelAdmin):
    pass

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass
