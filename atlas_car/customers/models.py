from django.db import models
from django.utils import timezone


class Customer(models.Model):
    CUSTOMER_TYPE_CHOICES = [
        ('individual', 'Individual'),
        ('company', 'Company'),
        ('partner_agency', 'Partner Agency'),
    ]

    cin = models.CharField(max_length=20, unique=True, verbose_name='National ID / Passport')
    passport = models.CharField(max_length=20, blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    nationality = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    license_number = models.CharField(max_length=50)
    license_expiration = models.DateField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField(blank=True)
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPE_CHOICES, default='individual')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def is_license_expired(self):
        return self.license_expiration < timezone.now().date()

    def total_rentals(self):
        return self.reservation_set.count()
