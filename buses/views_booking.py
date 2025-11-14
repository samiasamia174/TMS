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
    """Book a seat on a schedule"""
    schedule = get_object_or_404(Schedule, id=schedule_id)
    
    if request.method == 'POST':
        try:
            # For now, auto-assign next available seat
            booked_seats = Booking.objects.filter(schedule=schedule).values_list('seat_number', flat=True)
            all_seats = list(range(1, schedule.bus.capacity + 1))
            available_seats = [seat for seat in all_seats if seat not in booked_seats]
            
            if available_seats:
                seat_number = available_seats[0]
                
                # Create booking
                booking = Booking.objects.create(
                    user=request.user,
                    schedule=schedule,
                    seat_number=seat_number,
                    status='confirmed'
                )
                
                # Update available seats
                schedule.available_seats -= 1
                schedule.save()
                
                messages.success(request, f'Booking confirmed! Seat {seat_number} on {schedule.bus.bus_number}')
                return redirect('my_bookings')
            else:
                messages.error(request, 'No seats available on this bus')
                return redirect('route_schedules', route_id=schedule.route.id)
                
        except Exception as e:
            messages.error(request, f'Booking failed: {str(e)}')
            return redirect('route_schedules', route_id=schedule.route.id)
    
    return redirect('booking_list')

@login_required
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
