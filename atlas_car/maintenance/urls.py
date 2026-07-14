from django.urls import path
from . import views

app_name = 'maintenance'

urlpatterns = [
    path('', views.maintenance_list, name='maintenance_list'),
    path('add/', views.maintenance_create, name='maintenance_create'),
    path('<int:pk>/edit/', views.maintenance_edit, name='maintenance_edit'),
    path('<int:pk>/delete/', views.maintenance_delete, name='maintenance_delete'),
    path('vehicle/<int:vehicle_id>/', views.vehicle_maintenance_history, name='vehicle_maintenance_history'),
]
