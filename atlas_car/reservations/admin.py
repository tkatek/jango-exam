from django.contrib import admin
from reservations.models import Reservation, ReservationOption

class ReservationOptionInline(admin.TabularInline):
    model = ReservationOption
    extra = 1

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['reservation_number', 'customer', 'vehicle', 'pickup_date', 'return_date', 'status', 'total']
    list_filter = ['status', 'pickup_date']
    search_fields = ['reservation_number', 'customer__first_name', 'customer__last_name']
    inlines = [ReservationOptionInline]
