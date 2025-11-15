# TMS/payments/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.make_payment, name='make_payment'),          # ← root of /payments/
    path('success/', views.payment_success, name='payment_success'),
]