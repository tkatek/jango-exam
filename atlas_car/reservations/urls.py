from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    path('', views.reservation_list, name='reservation_list'),
    path('add/', views.reservation_create, name='reservation_create'),
    path('<int:pk>/', views.reservation_detail, name='reservation_detail'),
    path('<int:pk>/confirm/', views.reservation_confirm, name='reservation_confirm'),
    path('<int:pk>/start/', views.reservation_start, name='reservation_start'),
    path('<int:pk>/complete/', views.reservation_complete, name='reservation_complete'),
    path('<int:pk>/cancel/', views.reservation_cancel, name='reservation_cancel'),
    path('calendar/', views.reservation_calendar, name='reservation_calendar'),
    path('api/available-vehicles/', views.available_vehicles_api, name='available_vehicles_api'),
]
