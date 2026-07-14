from django.db import models
from django.conf import settings
from django.utils import timezone


class ActivityLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=200)
    model_name = models.CharField(max_length=100)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    details = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user} - {self.action} - {self.model_name}"


class Alert(models.Model):
    ALERT_TYPES = [
        ('return_tomorrow', 'Vehicle Return Tomorrow'),
        ('late_return', 'Late Return'),
        ('maintenance', 'Maintenance Alert'),
        ('license_expiry', 'License Expiration'),
        ('deposit_return', 'Deposit Return Reminder'),
    ]
    alert_type = models.CharField(max_length=30, choices=ALERT_TYPES)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    vehicle = models.ForeignKey('vehicles.Vehicle', on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey('customers.Customer', on_delete=models.CASCADE, null=True, blank=True)
    reservation = models.ForeignKey('reservations.Reservation', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_alert_type_display()} - {self.message[:50]}"
