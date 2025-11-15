# views.py — আপডেটেড (অপশন 1)
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
from buses.models import Bus
from .models import Payment
import uuid

@login_required
def make_payment(request, bus_id):
    bus = get_object_or_404(Bus, id=bus_id)
    amount = 500  # বা bus.price যদি মডেলে থাকে

    if request.method == 'POST':
        # কার্ড ভ্যালিডেশন (ডেমোর জন্য স্কিপ করা যায়)
        try:
            # পেমেন্ট সেভ
            payment = Payment.objects.create(
                user=request.user,
                bus=bus,
                amount=amount,
                transaction_id=str(uuid.uuid4())[:12].upper(),
                status='completed'
            )

            # ইমেইল পাঠাও
            subject = "University Transport – Payment Receipt"
            text_content = f"Thank you {request.user.get_full_name() or request.user.username}! Your payment of {amount} BDT is confirmed."
            html_content = render_to_string('payments/receipt_email.html', {
                'student_name': request.user.get_full_name() or request.user.username,
                'student_id': request.user.username,
                'vehicle_type': bus.bus_type,
                'bus_number': bus.bus_number,
                'amount': amount,
                'transaction_id': payment.transaction_id,
            })

            msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [request.user.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            messages.success(request, "Payment successful! A receipt has been sent to your email.")
            return redirect('payment_success')

        except Exception as e:
            messages.error(request, f"Payment failed: {str(e)}")
            print("Error:", e)

    return render(request, 'payments/payment_form.html', {
        'form': PaymentForm(),
        'bus': bus,
        'amount': amount,
    })