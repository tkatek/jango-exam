from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('', views.payment_list, name='payment_list'),
    path('add/', views.payment_create, name='payment_create'),
    path('<int:pk>/receipt/', views.payment_receipt, name='payment_receipt'),
    path('deposits/', views.deposit_list, name='deposit_list'),
    path('deposits/add/', views.deposit_create, name='deposit_create'),
    path('deposits/<int:pk>/return/', views.deposit_return, name='deposit_return'),
]
