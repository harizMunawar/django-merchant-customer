from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core.models import User, Merchant, Customer
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        ('Login Credential', {'fields': ('username', 'password')}),
        ('Profile', {'fields': ('is_merchant', 'is_customer', 'is_superuser')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_merchant', 'is_customer', 'is_superuser'),
        }),
    )
    list_filter = ()
    filter_horizontal = ()
    search_fields = ('username',)
    list_display = ('username', 'is_merchant', 'is_customer', 'is_superuser')

admin.site.unregister(Group)

@admin.register(Merchant)
class MerchantAdmin(admin.ModelAdmin):
    pass

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass
