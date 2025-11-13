# payments/views.py
from django.shortcuts import render, redirect
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages

def make_payment(request):
    if request.method == 'POST':
        student_name = request.POST.get('student_name')
        student_id = request.POST.get('student_id')
        vehicle_type = request.POST.get('vehicle_type')
        amount = request.POST.get('amount', '500')
        email = request.POST.get('email')

        # Simulate successful payment (no real gateway yet)

        # Render email content
        subject = "University Transport – Payment Receipt"
        text_content = f"Thank you {student_name}! Your payment of {amount} BDT is confirmed."
        html_content = render_to_string('payments/receipt_email.html', {
            'student_name': student_name,
            'student_id': student_id,
            'vehicle_type': vehicle_type,
            'amount': amount,
            'email': email,
        })

        # Send email
        msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        messages.success(request, "Payment successful! A receipt has been sent to your email.")
        return redirect('payment_success')

    return render(request, 'payments/payment_form.html')

def payment_success(request):
    return render(request, 'payments/payment_success.html')
