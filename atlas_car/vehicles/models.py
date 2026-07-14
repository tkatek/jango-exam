from django.db import models
from django.core.validators import RegexValidator


class Vehicle(models.Model):
    CATEGORY_CHOICES = [
        ('city', 'City'),
        ('suv', 'SUV'),
        ('sedan', 'Sedan'),
        ('utility', 'Utility'),
        ('luxury', 'Luxury'),
    ]
    TRANSMISSION_CHOICES = [
        ('manual', 'Manual'),
        ('automatic', 'Automatic'),
    ]
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('rented', 'Rented'),
        ('maintenance', 'Maintenance'),
        ('out_of_service', 'Out of Service'),
    ]

    license_plate = models.CharField(
        max_length=20, unique=True,
        validators=[RegexValidator(r'^[A-Z0-9\-]+$', 'Enter a valid license plate.')],
        verbose_name='License Plate'
    )
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    color = models.CharField(max_length=50)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES)
    seats = models.PositiveIntegerField(default=5)
    mileage = models.PositiveIntegerField(default=0)
    last_revision = models.DateField(null=True, blank=True)
    daily_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Daily Price (MAD)')
    deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Security Deposit (MAD)')
    photo = models.ImageField(upload_to='vehicles/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    maintenance_threshold = models.PositiveIntegerField(default=10000, help_text='Mileage threshold for maintenance alert')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.brand} {self.model} ({self.license_plate})"

    def needs_maintenance(self):
        return self.mileage >= self.maintenance_threshold

    def total_maintenance_cost(self):
        return self.maintenance_set.aggregate(total=models.Sum('cost'))['total'] or 0


class VehicleOption(models.Model):
    name = models.CharField(max_length=100)
    daily_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.daily_price} MAD/day)"
