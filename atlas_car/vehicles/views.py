from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Vehicle, VehicleOption
from .forms import VehicleForm, VehicleFilterForm, VehicleOptionForm


@login_required
def vehicle_list(request):
    vehicles = Vehicle.objects.all()
    form = VehicleFilterForm(request.GET)

    if form.is_valid():
        if form.cleaned_data.get('category'):
            vehicles = vehicles.filter(category=form.cleaned_data['category'])
        if form.cleaned_data.get('status'):
            vehicles = vehicles.filter(status=form.cleaned_data['status'])
        if form.cleaned_data.get('brand'):
            vehicles = vehicles.filter(brand__icontains=form.cleaned_data['brand'])
        if form.cleaned_data.get('transmission'):
            vehicles = vehicles.filter(transmission=form.cleaned_data['transmission'])

    stats = {
        'total': Vehicle.objects.count(),
        'available': Vehicle.objects.filter(status='available').count(),
        'rented': Vehicle.objects.filter(status='rented').count(),
        'maintenance': Vehicle.objects.filter(status='maintenance').count(),
        'out_of_service': Vehicle.objects.filter(status='out_of_service').count(),
    }
    return render(request, 'vehicles/vehicle_list.html', {
        'vehicles': vehicles, 'filter_form': form, 'stats': stats
    })


@login_required
def vehicle_detail(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    from maintenance.models import Maintenance
    maintenance_history = Maintenance.objects.filter(vehicle=vehicle)
    total_maintenance = sum(m.cost for m in maintenance_history)
    return render(request, 'vehicles/vehicle_detail.html', {
        'vehicle': vehicle,
        'maintenance_history': maintenance_history,
        'total_maintenance': total_maintenance,
    })


@login_required
def vehicle_create(request):
    if not hasattr(request.user, 'profile') or not request.user.profile.is_admin():
        messages.error(request, 'Only administrators can add vehicles.')
        return redirect('vehicles:vehicle_list')
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            vehicle = form.save()
            messages.success(request, f'Vehicle {vehicle} created successfully.')
            return redirect('vehicles:vehicle_detail', pk=vehicle.pk)
    else:
        form = VehicleForm()
    return render(request, 'vehicles/vehicle_form.html', {'form': form, 'title': 'Add Vehicle'})


@login_required
def vehicle_edit(request, pk):
    if not hasattr(request.user, 'profile') or not request.user.profile.is_admin():
        messages.error(request, 'Only administrators can edit vehicles.')
        return redirect('vehicles:vehicle_list')
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES, instance=vehicle)
        if form.is_valid():
            form.save()
            messages.success(request, f'Vehicle {vehicle} updated successfully.')
            return redirect('vehicles:vehicle_detail', pk=vehicle.pk)
    else:
        form = VehicleForm(instance=vehicle)
    return render(request, 'vehicles/vehicle_form.html', {'form': form, 'title': 'Edit Vehicle', 'vehicle': vehicle})


@login_required
def vehicle_delete(request, pk):
    if not hasattr(request.user, 'profile') or not request.user.profile.is_admin():
        messages.error(request, 'Only administrators can delete vehicles.')
        return redirect('vehicles:vehicle_list')
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == 'POST':
        vehicle.delete()
        messages.success(request, 'Vehicle deleted successfully.')
        return redirect('vehicles:vehicle_list')
    return render(request, 'vehicles/vehicle_confirm_delete.html', {'vehicle': vehicle})


@login_required
def option_list(request):
    options = VehicleOption.objects.all()
    return render(request, 'vehicles/option_list.html', {'options': options})


@login_required
def option_create(request):
    if request.method == 'POST':
        form = VehicleOptionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Option created successfully.')
            return redirect('vehicles:option_list')
    else:
        form = VehicleOptionForm()
    return render(request, 'vehicles/option_form.html', {'form': form})


@login_required
def option_edit(request, pk):
    option = get_object_or_404(VehicleOption, pk=pk)
    if request.method == 'POST':
        form = VehicleOptionForm(request.POST, instance=option)
        if form.is_valid():
            form.save()
            messages.success(request, 'Option updated successfully.')
            return redirect('vehicles:option_list')
    else:
        form = VehicleOptionForm(instance=option)
    return render(request, 'vehicles/option_form.html', {'form': form})


@login_required
def option_delete(request, pk):
    option = get_object_or_404(VehicleOption, pk=pk)
    if request.method == 'POST':
        option.delete()
        messages.success(request, 'Option deleted successfully.')
        return redirect('vehicles:option_list')
    return render(request, 'vehicles/option_confirm_delete.html', {'option': option})
