# TMS/payments/views.py
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
            # Get user (assuming student_id = username)
            user = User.objects.get(username=student_id)

            # Get a bus (fallback to first if not found)
            bus = Bus.objects.filter(bus_type__icontains=vehicle_type).first()
            if not bus:
                bus = Bus.objects.first()
                if not bus:
                    messages.error(request, "No bus available. Add one in admin.")
                    return redirect('make_payment')

            # Save payment
            transaction_id = str(uuid.uuid4())[:12].upper()
            Payment.objects.create(
                user=user,
                bus=bus,
                amount=amount,
                transaction_id=transaction_id,
                status='completed'
            )

            # Render email
            subject = "University Transport – Payment Receipt"
            text_content = f"Thank you, {student_name}! Payment of {amount} BDT confirmed."
            html_content = render_to_string('payments/receipt_email.html', {
                'student_name': student_name,
                'student_id': student_id,
                'vehicle_type': vehicle_type,
                'amount': amount,
                'transaction_id': transaction_id,
            })

            # Send email
            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            messages.success(request, "Payment successful! Check console for email receipt.")
            return redirect('payment_success')

        except User.DoesNotExist:
            messages.error(request, "Student ID not found. Register first.")
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")

    return render(request, 'payments/payment_form.html')