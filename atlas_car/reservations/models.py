from django.db import models
from django.utils import timezone
from decimal import Decimal
import datetime


class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    PICKUP_LOCATION_CHOICES = [
        ('agency', 'Agency'),
        ('airport', 'Airport'),
        ('hotel_delivery', 'Hotel Delivery'),
    ]

    reservation_number = models.CharField(max_length=20, unique=True, blank=True)
    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE)
    vehicle = models.ForeignKey('vehicles.Vehicle', on_delete=models.CASCADE)
    pickup_date = models.DateField()
    return_date = models.DateField()
    pickup_location = models.CharField(max_length=20, choices=PICKUP_LOCATION_CHOICES, default='agency')
    return_location = models.CharField(max_length=20, choices=PICKUP_LOCATION_CHOICES, default='agency')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    vat = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    options = models.ManyToManyField('vehicles.VehicleOption', through='ReservationOption', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.reservation_number} - {self.customer}"

    def save(self, *args, **kwargs):
        if not self.reservation_number:
            year = timezone.now().year
            last = Reservation.objects.filter(
                reservation_number__startswith=f'RES-{year}'
            ).order_by('-reservation_number').first()
            if last:
                num = int(last.reservation_number.split('-')[-1]) + 1
            else:
                num = 1
            self.reservation_number = f'RES-{year}-{num:05d}'
        super().save(*args, **kwargs)

    def rental_days(self):
        delta = self.return_date - self.pickup_date
        return max(delta.days, 1)

    def calculate_totals(self):
        days = self.rental_days()
        vehicle_cost = self.vehicle.daily_price * Decimal(days)
        options_cost = sum(
            opt.option.daily_price * Decimal(days) * opt.quantity
            for opt in self.reservationoption_set.all()
        )
        self.subtotal = vehicle_cost + options_cost
        self.vat = self.subtotal * Decimal('0.20')
        self.total = self.subtotal + self.vat
        self.deposit = self.vehicle.deposit
        self.save()

    def is_overlapping(self):
        return Reservation.objects.filter(
            vehicle=self.vehicle,
            status__in=['confirmed', 'active'],
            pickup_date__lt=self.return_date,
            return_date__gt=self.pickup_date,
        ).exclude(pk=self.pk).exists()

    def can_confirm(self):
        return self.status == 'pending'

    def can_start(self):
        return self.status == 'confirmed' and self.pickup_date <= timezone.now().date()

    def can_complete(self):
        return self.status == 'active'

    def can_cancel(self):
        return self.status in ['pending', 'confirmed']


class ReservationOption(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    option = models.ForeignKey('vehicles.VehicleOption', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.option} x{self.quantity}"
