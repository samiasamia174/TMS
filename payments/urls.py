# payments/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('payment/', views.make_payment, name='make_payment'),
    path('payment/success/', views.payment_success, name='payment_success'),
]
