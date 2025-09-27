from django.shortcuts import render, get_object_or_404, redirect
from .models import Payment
from transport.models import Registration
from django.contrib.auth.decorators import login_required
from django.urls import reverse

@login_required
def checkout(request, registration_id):
    reg=get_object_or_404(Registration,id=registration_id)
    if request.method=='POST':
        payment, _ = Payment.objects.get_or_create(registration=reg, defaults={'amount':50.00,'status':'completed','transaction_id':'SIM123'})
        payment.status='completed'
        payment.transaction_id=f"SIM-{payment.id}"
        payment.save()
        return redirect(reverse('payments:success',kwargs={'payment_id':payment.id}))
    return render(request,'payments/checkout.html',{'registration':reg})

@login_required
def success(request,payment_id):
    payment=get_object_or_404(Payment,id=payment_id)
    return render(request,'payments/success.html',{'payment':payment})
