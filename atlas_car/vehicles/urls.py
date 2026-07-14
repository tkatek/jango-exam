from django.urls import path
from . import views

app_name = 'vehicles'

urlpatterns = [
    path('', views.vehicle_list, name='vehicle_list'),
    path('add/', views.vehicle_create, name='vehicle_create'),
    path('<int:pk>/', views.vehicle_detail, name='vehicle_detail'),
    path('<int:pk>/edit/', views.vehicle_edit, name='vehicle_edit'),
    path('<int:pk>/delete/', views.vehicle_delete, name='vehicle_delete'),
    path('options/', views.option_list, name='option_list'),
    path('options/add/', views.option_create, name='option_create'),
    path('options/<int:pk>/edit/', views.option_edit, name='option_edit'),
    path('options/<int:pk>/delete/', views.option_delete, name='option_delete'),
]
