from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Maintenance
from .forms import MaintenanceForm
from vehicles.models import Vehicle


@login_required
def maintenance_list(request):
    records = Maintenance.objects.select_related('vehicle').all()
    return render(request, 'maintenance/maintenance_list.html', {'records': records})


@login_required
def maintenance_create(request):
    if request.method == 'POST':
        form = MaintenanceForm(request.POST)
        if form.is_valid():
            record = form.save()
            messages.success(request, 'Maintenance record created.')
            return redirect('maintenance:maintenance_list')
    else:
        form = MaintenanceForm()
    return render(request, 'maintenance/maintenance_form.html', {'form': form})


@login_required
def maintenance_edit(request, pk):
    record = get_object_or_404(Maintenance, pk=pk)
    if request.method == 'POST':
        form = MaintenanceForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Maintenance record updated.')
            return redirect('maintenance:maintenance_list')
    else:
        form = MaintenanceForm(instance=record)
    return render(request, 'maintenance/maintenance_form.html', {'form': form})


@login_required
def maintenance_delete(request, pk):
    record = get_object_or_404(Maintenance, pk=pk)
    if request.method == 'POST':
        record.delete()
        messages.success(request, 'Maintenance record deleted.')
        return redirect('maintenance:maintenance_list')
    return render(request, 'maintenance/maintenance_confirm_delete.html', {'record': record})


@login_required
def vehicle_maintenance_history(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
    records = Maintenance.objects.filter(vehicle=vehicle)
    total = sum(m.cost for m in records)
    return render(request, 'maintenance/vehicle_maintenance_history.html', {
        'vehicle': vehicle, 'records': records, 'total': total
    })
