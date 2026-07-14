from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum, Count
from datetime import timedelta
from vehicles.models import Vehicle
from customers.models import Customer
from reservations.models import Reservation
from payments.models import Payment
from invoices.models import Invoice
from core.models import Alert
import json


@login_required
def home(request):
    today = timezone.now().date()
    month_start = today.replace(day=1)

    total_vehicles = Vehicle.objects.count()
    available_vehicles = Vehicle.objects.filter(status='available').count()
    rented_vehicles = Vehicle.objects.filter(status='rented').count()

    total_reservations = Reservation.objects.count()
    today_reservations = Reservation.objects.filter(pickup_date=today).count()
    active_reservations = Reservation.objects.filter(status='active').count()

    monthly_revenue = Payment.objects.filter(
        payment_date__gte=month_start
    ).aggregate(total=Sum('amount'))['total'] or 0

    yearly_revenue = Payment.objects.filter(
        payment_date__year=today.year
    ).aggregate(total=Sum('amount'))['total'] or 0

    recent_reservations = Reservation.objects.select_related(
        'customer', 'vehicle'
    )[:5]

    upcoming_returns = Reservation.objects.filter(
        return_date__gte=today,
        return_date__lte=today + timedelta(days=1),
        status='active'
    ).select_related('customer', 'vehicle')

    alerts = Alert.objects.filter(is_read=False)[:5]

    occupancy_rate = (rented_vehicles / total_vehicles * 100) if total_vehicles > 0 else 0

    return render(request, 'dashboard/home.html', {
        'total_vehicles': total_vehicles,
        'available_vehicles': available_vehicles,
        'rented_vehicles': rented_vehicles,
        'total_reservations': total_reservations,
        'today_reservations': today_reservations,
        'active_reservations': active_reservations,
        'monthly_revenue': monthly_revenue,
        'yearly_revenue': yearly_revenue,
        'recent_reservations': recent_reservations,
        'upcoming_returns': upcoming_returns,
        'alerts': alerts,
        'occupancy_rate': round(occupancy_rate, 1),
    })


@login_required
def dashboard_charts(request):
    today = timezone.now().date()

    monthly_data = []
    for i in range(12):
        month = today.month - i
        year = today.year
        if month <= 0:
            month += 12
            year -= 1
        revenue = Payment.objects.filter(
            payment_date__year=year, payment_date__month=month
        ).aggregate(total=Sum('amount'))['total'] or 0
        count = Reservation.objects.filter(
            pickup_date__year=year, pickup_date__month=month
        ).count()
        monthly_data.append({
            'month': f"{year}-{month:02d}",
            'revenue': float(revenue),
            'reservations': count,
        })
    monthly_data.reverse()

    category_data = list(
        Vehicle.objects.values('category').annotate(count=Count('id')).order_by('category')
    )

    status_data = list(
        Reservation.objects.values('status').annotate(count=Count('id')).order_by('status')
    )

    top_vehicles = list(
        Reservation.objects.values('vehicle__brand', 'vehicle__model')
        .annotate(count=Count('id'))
        .order_by('-count')[:5]
    )

    return render(request, 'dashboard/charts.html', {
        'monthly_data': json.dumps(monthly_data),
        'category_data': json.dumps(category_data),
        'status_data': json.dumps(status_data),
        'top_vehicles': json.dumps(top_vehicles),
    })
