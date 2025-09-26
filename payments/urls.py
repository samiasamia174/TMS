# payments/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Example endpoint
    path('', views.index, name='payments-index'),
]
