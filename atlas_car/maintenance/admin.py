from django.contrib import admin
from maintenance.models import Maintenance

@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ['vehicle', 'maintenance_type', 'garage', 'date', 'cost']
    list_filter = ['maintenance_type', 'date']
