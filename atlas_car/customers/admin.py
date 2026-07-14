from django.contrib import admin
from customers.models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'cin', 'phone', 'email', 'customer_type']
    search_fields = ['first_name', 'last_name', 'cin', 'passport']
    list_filter = ['customer_type', 'nationality']
