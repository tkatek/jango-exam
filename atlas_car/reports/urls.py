from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.reports_index, name='reports_index'),
    path('monthly/', views.monthly_activity_report, name='monthly_activity'),
    path('fleet/', views.fleet_report, name='fleet_report'),
    path('revenue/', views.revenue_report, name='revenue_report'),
    path('customers/', views.customer_report, name='customer_report'),
]
