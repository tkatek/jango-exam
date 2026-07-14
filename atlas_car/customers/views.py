from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Customer
from .forms import CustomerForm, CustomerSearchForm


@login_required
def customer_list(request):
    customers = Customer.objects.all()
    form = CustomerSearchForm(request.GET)
    if form.is_valid() and form.cleaned_data.get('query'):
        q = form.cleaned_data['query']
        customers = customers.filter(
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(cin__icontains=q) |
            Q(passport__icontains=q)
        )
    return render(request, 'customers/customer_list.html', {'customers': customers, 'form': form})


@login_required
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    from reservations.models import Reservation
    from payments.models import Payment
    from invoices.models import Invoice
    reservations = Reservation.objects.filter(customer=customer)
    payments = Payment.objects.filter(reservation__customer=customer)
    invoices = Invoice.objects.filter(reservation__customer=customer)
    return render(request, 'customers/customer_detail.html', {
        'customer': customer,
        'reservations': reservations,
        'payments': payments,
        'invoices': invoices,
        'total_rentals': reservations.count(),
    })


@login_required
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save()
            messages.success(request, f'Customer {customer} created successfully.')
            return redirect('customers:customer_detail', pk=customer.pk)
    else:
        form = CustomerForm()
    return render(request, 'customers/customer_form.html', {'form': form, 'title': 'Add Customer'})


@login_required
def customer_edit(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, f'Customer {customer} updated successfully.')
            return redirect('customers:customer_detail', pk=customer.pk)
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customers/customer_form.html', {'form': form, 'title': 'Edit Customer', 'customer': customer})


@login_required
def customer_delete(request, pk):
    if not hasattr(request.user, 'profile') or not request.user.profile.is_admin():
        messages.error(request, 'Only administrators can delete customers.')
        return redirect('customers:customer_list')
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        messages.success(request, 'Customer deleted successfully.')
        return redirect('customers:customer_list')
    return render(request, 'customers/customer_confirm_delete.html', {'customer': customer})
