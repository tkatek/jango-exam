from django.urls import path
from . import views

app_name = 'invoices'

urlpatterns = [
    path('', views.invoice_list, name='invoice_list'),
    path('<int:pk>/', views.invoice_detail, name='invoice_detail'),
    path('create/<int:reservation_id>/', views.invoice_create, name='invoice_create'),
    path('<int:pk>/pdf/', views.invoice_generate_pdf, name='invoice_pdf'),
]
