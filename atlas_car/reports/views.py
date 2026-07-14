from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum, Count
from vehicles.models import Vehicle
from customers.models import Customer
from reservations.models import Reservation
from payments.models import Payment


@login_required
def reports_index(request):
    return render(request, 'reports/reports_index.html')


@login_required
def monthly_activity_report(request):
    today = timezone.now().date()
    month_start = today.replace(day=1)
    reservations = Reservation.objects.filter(
        pickup_date__gte=month_start
    ).select_related('customer', 'vehicle')
    total_revenue = Payment.objects.filter(
        payment_date__gte=month_start
    ).aggregate(total=Sum('amount'))['total'] or 0
    return render(request, 'reports/monthly_activity.html', {
        'reservations': reservations,
        'total_revenue': total_revenue,
        'month': today.strftime('%B %Y'),
    })


@login_required
def fleet_report(request):
    vehicles = Vehicle.objects.all()
    stats = {
        'total': vehicles.count(),
        'available': vehicles.filter(status='available').count(),
        'rented': vehicles.filter(status='rented').count(),
        'maintenance': vehicles.filter(status='maintenance').count(),
        'out_of_service': vehicles.filter(status='out_of_service').count(),
    }
    return render(request, 'reports/fleet_report.html', {
        'vehicles': vehicles, 'stats': stats
    })


@login_required
def revenue_report(request):
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
        monthly_data.append({
            'month': f"{year}-{month:02d}",
            'revenue': float(revenue),
        })
    monthly_data.reverse()
    return render(request, 'reports/revenue_report.html', {'monthly_data': monthly_data})


@login_required
def customer_report(request):
    customers = Customer.objects.annotate(
        rental_count=Count('reservation')
    ).order_by('-rental_count')[:20]
    nationality_stats = Customer.objects.values('nationality').annotate(
        count=Count('id')
    ).order_by('-count')
    return render(request, 'reports/customer_report.html', {
        'customers': customers,
        'nationality_stats': nationality_stats,
    })
