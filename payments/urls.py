from django.urls import path
from . import views

app_name='payments'
urlpatterns=[
    path('checkout/<int:registration_id>/',views.checkout,name='checkout'),
    path('success/<int:payment_id>/',views.success,name='success'),
]
