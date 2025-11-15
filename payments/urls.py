# payments/urls.py
urlpatterns = [
    path('payment/<int:bus_id>/', views.make_payment, name='make_payment'),
    path('payment/success/', views.payment_success, name='payment_success'),
]