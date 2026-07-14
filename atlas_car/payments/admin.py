from django.contrib import admin
from payments.models import Payment, Deposit

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'reservation', 'method', 'amount', 'payment_date']
    list_filter = ['method', 'payment_date']

@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ['reservation', 'amount_received', 'amount_returned', 'return_date']
