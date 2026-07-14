from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Invoice
from reservations.models import Reservation
from decimal import Decimal


@login_required
def invoice_list(request):
    invoices = Invoice.objects.select_related('reservation__customer').all()
    return render(request, 'invoices/invoice_list.html', {'invoices': invoices})


@login_required
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    return render(request, 'invoices/invoice_detail.html', {'invoice': invoice})


@login_required
def invoice_create(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    if Invoice.objects.filter(reservation=reservation).exists():
        messages.warning(request, 'Invoice already exists for this reservation.')
        return redirect('invoices:invoice_list')
    invoice = Invoice.objects.create(
        reservation=reservation,
        subtotal=reservation.subtotal,
        vat=reservation.vat,
        total=reservation.total,
    )
    messages.success(request, f'Invoice {invoice.invoice_number} created.')
    return redirect('invoices:invoice_detail', pk=invoice.pk)


@login_required
def invoice_generate_pdf(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.pdfgen import canvas
        from reportlab.lib.units import cm
        import io
        from django.http import FileResponse

        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        p.setFont("Helvetica-Bold", 16)
        p.drawString(2*cm, height - 2*cm, "Atlas Car Location")
        p.setFont("Helvetica", 10)
        p.drawString(2*cm, height - 3*cm, "Car Rental Invoice")

        p.setFont("Helvetica-Bold", 12)
        p.drawString(2*cm, height - 5*cm, f"Invoice Number: {invoice.invoice_number}")
        p.drawString(2*cm, height - 6*cm, f"Date: {invoice.created_at.strftime('%d/%m/%Y')}")

        p.setFont("Helvetica-Bold", 11)
        p.drawString(2*cm, height - 8*cm, "Customer Information")
        p.setFont("Helvetica", 10)
        customer = invoice.reservation.customer
        p.drawString(2*cm, height - 9*cm, f"Name: {customer.first_name} {customer.last_name}")
        p.drawString(2*cm, height - 9.5*cm, f"CIN: {customer.cin}")
        p.drawString(2*cm, height - 10*cm, f"Phone: {customer.phone}")

        p.setFont("Helvetica-Bold", 11)
        p.drawString(2*cm, height - 12*cm, "Vehicle Information")
        p.setFont("Helvetica", 10)
        vehicle = invoice.reservation.vehicle
        p.drawString(2*cm, height - 13*cm, f"Vehicle: {vehicle.brand} {vehicle.model}")
        p.drawString(2*cm, height - 13.5*cm, f"License Plate: {vehicle.license_plate}")
        p.drawString(2*cm, height - 14*cm, f"Rental Days: {invoice.reservation.rental_days()}")
        p.drawString(2*cm, height - 14.5*cm, f"Daily Price: {vehicle.daily_price} MAD")

        p.setFont("Helvetica-Bold", 11)
        p.drawString(2*cm, height - 16.5*cm, "Financial Details")
        p.setFont("Helvetica", 10)
        p.drawString(2*cm, height - 17.5*cm, f"Subtotal: {invoice.subtotal} MAD")
        p.drawString(2*cm, height - 18*cm, f"VAT (20%): {invoice.vat} MAD")
        p.setFont("Helvetica-Bold", 11)
        p.drawString(2*cm, height - 19*cm, f"Total: {invoice.total} MAD")

        p.setFont("Helvetica", 8)
        p.drawString(2*cm, 3*cm, "Atlas Car Location - Legal Notice: This is a computer-generated invoice.")
        p.drawString(2*cm, 2.5*cm, f"Company Stamp Area")

        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=f'{invoice.invoice_number}.pdf')
    except ImportError:
        messages.error(request, 'ReportLab is required to generate PDF invoices.')
        return redirect('invoices:invoice_detail', pk=pk)
