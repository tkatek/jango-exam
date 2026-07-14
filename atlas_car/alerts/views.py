from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from core.models import Alert
from reservations.models import Reservation
from vehicles.models import Vehicle
from customers.models import Customer


@login_required
def alert_list(request):
    alerts = Alert.objects.all()
    return render(request, 'alerts/alert_list.html', {'alerts': alerts})


@login_required
def alert_mark_read(request, pk):
    alert = Alert.objects.get(pk=pk)
    alert.is_read = True
    alert.save()
    return redirect('alerts:alert_list')


@login_required
def alert_mark_all_read(request):
    Alert.objects.filter(is_read=False).update(is_read=True)
    messages.success(request, 'All alerts marked as read.')
    return redirect('alerts:alert_list')


@login_required
def generate_alerts(request):
    today = timezone.now().date()

    Reservation.objects.filter(
        return_date=today + timedelta(days=1),
        status='active'
    ).select_related('customer', 'vehicle').update()

    for res in Reservation.objects.filter(
        return_date=today + timedelta(days=1),
        status='active'
    ):
        Alert.objects.get_or_create(
            alert_type='return_tomorrow',
            reservation=res,
            defaults={
                'message': f"Vehicle {res.vehicle} is due for return tomorrow. Customer: {res.customer}",
                'vehicle': res.vehicle,
                'customer': res.customer,
            }
        )

    for res in Reservation.objects.filter(
        return_date__lt=today,
        status='active'
    ):
        Alert.objects.get_or_create(
            alert_type='late_return',
            reservation=res,
            defaults={
                'message': f"LATE RETURN: Vehicle {res.vehicle} was due on {res.return_date}. Customer: {res.customer}",
                'vehicle': res.vehicle,
                'customer': res.customer,
            }
        )

    for vehicle in Vehicle.objects.filter(status='available'):
        if vehicle.needs_maintenance():
            Alert.objects.get_or_create(
                alert_type='maintenance',
                vehicle=vehicle,
                defaults={
                    'message': f"Maintenance needed: {vehicle} has {vehicle.mileage}km (threshold: {vehicle.maintenance_threshold}km)",
                    'vehicle': vehicle,
                }
            )

    for customer in Customer.objects.all():
        if customer.license_expiration <= today + timedelta(days=30):
            Alert.objects.get_or_create(
                alert_type='license_expiry',
                customer=customer,
                defaults={
                    'message': f"License expiring soon: {customer} - expires {customer.license_expiration}",
                    'customer': customer,
                }
            )

    messages.success(request, 'Alerts generated successfully.')
    return redirect('alerts:alert_list')
