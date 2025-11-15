from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Route, Bus, Schedule, Booking
from django.http import JsonResponse
import json

@login_required
def booking_list(request):
    """Main booking page - show available routes"""
    routes = Route.objects.filter(is_active=True)
    return render(request, 'booking/list.html', {'routes': routes})

@login_required
def route_schedules(request, route_id):
    """Show schedules for a specific route"""
    route = get_object_or_404(Route, id=route_id)
    schedules = Schedule.objects.filter(route=route, available_seats__gt=0)
    return render(request, 'booking/schedules.html', {
        'route': route,
        'schedules': schedules
    })

@login_required

def book_seat(request, schedule_id):
    """Book a seat on a schedule without specific seat number"""
    from django.shortcuts import get_object_or_404, redirect
    from django.contrib import messages
    from .models import Schedule, Booking
    import uuid
    
    if not request.user.is_authenticated:
        messages.error(request, 'Please login to book a seat.')
        return redirect('signin')
    
    schedule = get_object_or_404(Schedule, id=schedule_id)
    
    # Check if seats are available
    if schedule.available_seats <= 0:
        messages.error(request, 'No seats available on this bus.')
        return redirect('route_schedules', route_id=schedule.route.id)
    
    try:
        # Create booking without specific seat number
        booking = Booking.objects.create(
            booking_id=uuid.uuid4(),
            user=request.user,
            schedule=schedule,
            passengers=1,  # Default to 1 passenger
            total_amount=schedule.route.fare,
            payment_status='pending',
            is_confirmed=False
        )
        
        # Update available seats
        schedule.available_seats -= 1
        schedule.save()
        
        messages.success(request, f'Booking successful! Your booking ID is {booking.booking_id}')
        return redirect('my_bookings')
        
    except Exception as e:
        messages.error(request, f'Booking failed: {str(e)}')
        return redirect('route_schedules', route_id=schedule.route.id)
def my_bookings(request):
    """Show user's bookings"""
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    return render(request, 'booking/my_bookings.html', {'bookings': bookings})

@login_required
def cancel_booking(request, booking_id):
    """Cancel a booking"""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.status != 'cancelled':
        booking.status = 'cancelled'
        booking.save()
        
        # Return seat to available seats
        schedule = booking.schedule
        schedule.available_seats += 1
        schedule.save()
        
        messages.success(request, 'Booking cancelled successfully')
    
    return redirect('my_bookings')
