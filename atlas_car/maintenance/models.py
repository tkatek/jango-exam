from django.db import models


class Maintenance(models.Model):
    TYPE_CHOICES = [
        ('oil_change', 'Oil Change'),
        ('tire_change', 'Tire Change'),
        ('brake_service', 'Brake Service'),
        ('engine_repair', 'Engine Repair'),
        ('body_repair', 'Body Repair'),
        ('revision', 'Revision'),
        ('other', 'Other'),
    ]

    vehicle = models.ForeignKey('vehicles.Vehicle', on_delete=models.CASCADE)
    maintenance_type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    garage = models.CharField(max_length=200)
    date = models.DateField()
    mileage = models.PositiveIntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.get_maintenance_type_display()} - {self.vehicle} ({self.date})"
