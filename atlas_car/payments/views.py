from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Payment, Deposit
from .forms import PaymentForm, DepositForm
from reservations.models import Reservation


@login_required
def payment_list(request):
    payments = Payment.objects.select_related('reservation').all()
    return render(request, 'payments/payment_list.html', {'payments': payments})


@login_required
def payment_create(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save()
            messages.success(request, f'Payment of {payment.amount} MAD recorded.')
            return redirect('payments:payment_list')
    else:
        form = PaymentForm()
    return render(request, 'payments/payment_form.html', {'form': form})


@login_required
def payment_receipt(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
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
        p.drawString(2*cm, height - 3*cm, "Payment Receipt")

        p.setFont("Helvetica-Bold", 11)
        p.drawString(2*cm, height - 5*cm, f"Receipt Number: PAY-{payment.id:05d}")
        p.drawString(2*cm, height - 6*cm, f"Date: {payment.payment_date.strftime('%d/%m/%Y')}")

        p.setFont("Helvetica", 10)
        p.drawString(2*cm, height - 8*cm, f"Reservation: {payment.reservation.reservation_number}")
        p.drawString(2*cm, height - 9*cm, f"Method: {payment.get_method_display()}")
        p.drawString(2*cm, height - 10*cm, f"Amount: {payment.amount} MAD")
        if payment.reference:
            p.drawString(2*cm, height - 11*cm, f"Reference: {payment.reference}")

        p.setFont("Helvetica", 8)
        p.drawString(2*cm, 3*cm, "Atlas Car Location - Thank you for your payment.")

        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=f'receipt-{payment.id}.pdf')
    except ImportError:
        messages.error(request, 'ReportLab is required to generate receipts.')
        return redirect('payments:payment_list')


@login_required
def deposit_list(request):
    deposits = Deposit.objects.select_related('reservation').all()
    return render(request, 'payments/deposit_list.html', {'deposits': deposits})


@login_required
def deposit_create(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            deposit = form.save()
            messages.success(request, 'Deposit recorded successfully.')
            return redirect('payments:deposit_list')
    else:
        form = DepositForm()
    return render(request, 'payments/deposit_form.html', {'form': form})


@login_required
def deposit_return(request, pk):
    deposit = get_object_or_404(Deposit, pk=pk)
    if request.method == 'POST':
        from django.utils import timezone
        deposit.amount_returned = deposit.amount_received
        deposit.return_date = timezone.now().date()
        deposit.save()
        messages.success(request, 'Deposit returned successfully.')
        return redirect('payments:deposit_list')
    return render(request, 'payments/deposit_return.html', {'deposit': deposit})
