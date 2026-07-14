from django.contrib import admin
from invoices.models import Invoice

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'reservation', 'subtotal', 'vat', 'total', 'created_at']
    search_fields = ['invoice_number']
