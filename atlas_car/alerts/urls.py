from django.urls import path
from . import views

app_name = 'alerts'

urlpatterns = [
    path('', views.alert_list, name='alert_list'),
    path('<int:pk>/read/', views.alert_mark_read, name='alert_mark_read'),
    path('all-read/', views.alert_mark_all_read, name='alert_mark_all_read'),
    path('generate/', views.generate_alerts, name='generate_alerts'),
]
