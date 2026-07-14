from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from .models import Reservation, ReservationOption
from .forms import ReservationForm, ReservationOptionFormSet
from vehicles.models import Vehicle
from customers.models import Customer
from datetime import timedelta


@login_required
def reservation_list(request):
    reservations = Reservation.objects.select_related('customer', 'vehicle').all()
    status_filter = request.GET.get('status')
    if status_filter:
        reservations = reservations.filter(status=status_filter)
    return render(request, 'reservations/reservation_list.html', {
        'reservations': reservations, 'status_filter': status_filter
    })


@login_required
def reservation_detail(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    from payments.models import Payment
    payments = Payment.objects.filter(reservation=reservation)
    total_paid = sum(p.amount for p in payments)
    return render(request, 'reservations/reservation_detail.html', {
        'reservation': reservation, 'payments': payments, 'total_paid': total_paid
    })


@login_required
def reservation_create(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        formset = ReservationOptionFormSet(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            customer = reservation.customer
            if customer.is_license_expired():
                messages.error(request, 'Cannot create reservation: customer driving license is expired.')
                return redirect('reservations:reservation_create')
            if reservation.is_overlapping():
                messages.error(request, 'Cannot create reservation: vehicle is already reserved for these dates.')
                return redirect('reservations:reservation_create')
            reservation.save()
            formset = ReservationOptionFormSet(request.POST, instance=reservation)
            if formset.is_valid():
                formset.save()
            reservation.calculate_totals()
            messages.success(request, f'Reservation {reservation.reservation_number} created successfully.')
            return redirect('reservations:reservation_detail', pk=reservation.pk)
    else:
        form = ReservationForm()
        formset = ReservationOptionFormSet()
    return render(request, 'reservations/reservation_form.html', {'form': form, 'formset': formset})


@login_required
def reservation_confirm(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if reservation.can_confirm():
        reservation.status = 'confirmed'
        reservation.save()
        messages.success(request, f'Reservation {reservation.reservation_number} confirmed.')
    return redirect('reservations:reservation_detail', pk=pk)


@login_required
def reservation_start(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if reservation.can_start():
        reservation.status = 'active'
        reservation.vehicle.status = 'rented'
        reservation.vehicle.save()
        reservation.save()
        messages.success(request, f'Reservation {reservation.reservation_number} started.')
    return redirect('reservations:reservation_detail', pk=pk)


@login_required
def reservation_complete(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if reservation.can_complete():
        reservation.status = 'completed'
        reservation.vehicle.status = 'available'
        reservation.vehicle.save()
        reservation.save()
        messages.success(request, f'Reservation {reservation.reservation_number} completed.')
    return redirect('reservations:reservation_detail', pk=pk)


@login_required
def reservation_cancel(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    if reservation.can_cancel():
        reservation.status = 'cancelled'
        if reservation.vehicle.status == 'rented':
            reservation.vehicle.status = 'available'
            reservation.vehicle.save()
        reservation.save()
        messages.success(request, f'Reservation {reservation.reservation_number} cancelled.')
    return redirect('reservations:reservation_detail', pk=pk)


@login_required
def reservation_calendar(request):
    year = int(request.GET.get('year', timezone.now().year))
    month = int(request.GET.get('month', timezone.now().month))
    import datetime as _dt
    start_date = _dt.date(year, month, 1)
    if month == 12:
        end_date = _dt.date(year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = _dt.date(year, month + 1, 1) - timedelta(days=1)

    reservations = Reservation.objects.filter(
        pickup_date__lte=end_date,
        return_date__gte=start_date,
        status__in=['pending', 'confirmed', 'active']
    ).select_related('customer', 'vehicle')

    return render(request, 'reservations/reservation_calendar.html', {
        'reservations': reservations, 'year': year, 'month': month,
    })


@login_required
def available_vehicles_api(request):
    pickup = request.GET.get('pickup_date')
    return_date = request.GET.get('return_date')
    if pickup and return_date:
        reserved_ids = Reservation.objects.filter(
            pickup_date__lt=return_date,
            return_date__gt=pickup,
            status__in=['confirmed', 'active']
        ).values_list('vehicle_id', flat=True)
        vehicles = Vehicle.objects.filter(status='available').exclude(id__in=reserved_ids)
    else:
        vehicles = Vehicle.objects.filter(status='available')
    data = [{'id': v.id, 'name': str(v), 'daily_price': str(v.daily_price)} for v in vehicles]
    return JsonResponse({'vehicles': data})
