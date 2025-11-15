# payments/views.py
from django.shortcuts import render, redirect
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from buses.models import Bus
from .models import Payment
import uuid

def make_payment(request):
    if request.method == 'POST':
        student_name = request.POST.get('student_name')
        student_id = request.POST.get('student_id')
        vehicle_type = request.POST.get('vehicle_type')
        amount = request.POST.get('amount', '500')
        email = request.POST.get('email')

        try:
            # 1. ইউজার খুঁজো (যেহেতু Payment মডেলে user ForeignKey)
            user = User.objects.get(username=student_id)  # ধরে নিচ্ছি student_id == username

            # 2. Bus খুঁজো (যেহেতু bus ForeignKey)
            bus = Bus.objects.filter(bus_type=vehicle_type).first()
            if not bus:
                bus = Bus.objects.first()  # fallback
                if not bus:
                    messages.error(request, "No bus available. Please add a bus in admin.")
                    return redirect('make_payment')

            # 3. পেমেন্ট অবজেক্ট তৈরি করো
            transaction_id = str(uuid.uuid4())[:12].upper()
            payment = Payment.objects.create(
                user=user,
                bus=bus,
                amount=amount,
                transaction_id=transaction_id,
                status='completed'
            )

            # 4. ইমেইল পাঠাও
            subject = "University Transport – Payment Receipt"
            text_content = f"Thank you {student_name}! Your payment of {amount} BDT is confirmed."
            html_content = render_to_string('payments/receipt_email.html', {
                'student_name': student_name,
                'student_id': student_id,
                'vehicle_type': vehicle_type,
                'amount': amount,
                'transaction_id': transaction_id,
            })

            msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            messages.success(request, "Payment successful! A receipt has been sent to your email.")
            return redirect('payment_success')

        except User.DoesNotExist:
            messages.error(request, "Student ID not found. Please register first.")
        except Exception as e:
            messages.error(request, f"Payment failed: {str(e)}")
            # Optional: log error in console
            print("Email/Payment error:", e)

        return render(request, 'payments/payment_form.html')