from django.db import models
from django.utils import timezone


class Invoice(models.Model):
    invoice_number = models.CharField(max_length=20, unique=True, blank=True)
    reservation = models.OneToOneField('reservations.Reservation', on_delete=models.CASCADE)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    vat = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    pdf = models.FileField(upload_to='invoices/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.invoice_number

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            year = timezone.now().year
            last = Invoice.objects.filter(
                invoice_number__startswith=f'INV-{year}'
            ).order_by('-invoice_number').first()
            if last:
                num = int(last.invoice_number.split('-')[-1]) + 1
            else:
                num = 1
            self.invoice_number = f'INV-{year}-{num:05d}'
        super().save(*args, **kwargs)
