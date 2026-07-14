from django.contrib import admin
from vehicles.models import Vehicle, VehicleOption

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['license_plate', 'brand', 'model', 'category', 'status', 'daily_price']
    list_filter = ['status', 'category', 'transmission']
    search_fields = ['license_plate', 'brand', 'model']

@admin.register(VehicleOption)
class VehicleOptionAdmin(admin.ModelAdmin):
    list_display = ['name', 'daily_price']
