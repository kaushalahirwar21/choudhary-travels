import math
import urllib.parse
from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from django.utils import timezone

from geopy.geocoders import Nominatim
from geopy.distance import geodesic

from .models import Car, Booking


# HOME PAGE
def home(request):
    return render(request, 'home.html')


def book(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        phone = request.POST.get('phone')
        pickup = request.POST.get('pickup')
        drop = request.POST.get('drop')
        start_time = request.POST.get('start_time')

        # ✅ Basic validation
        if not name or not phone or not start_time:
            return render(request, 'book.html', {
                'error': '❌ All fields are required'
            })

        # ✅ Convert time
        start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M")
        start_time = timezone.make_aware(start_time)

        # ✅ Duration (dynamic)
        duration_hours = int(request.POST.get('hours', 2))
        end_time = start_time + timedelta(hours=duration_hours)

        # ✅ Calculate distance
        geolocator = Nominatim(user_agent="choudhary_travels")
        try:
            pickup_location = geolocator.geocode(pickup)
            drop_location = geolocator.geocode(drop)
            if not pickup_location or not drop_location:
                return render(request, 'book.html', {
                    'error': '❌ Unable to find locations. Please enter valid addresses.'
                })
            distance = geodesic((pickup_location.latitude, pickup_location.longitude), (drop_location.latitude, drop_location.longitude)).km
        except Exception as e:
            return render(request, 'book.html', {
                'error': '❌ Error calculating distance. Please try again.'
            })

        # ✅ Get car
        car = Car.objects.first()
        if not car:
            return render(request, 'book.html', {
                'error': '❌ No cars available'
            })

        # ✅ Conflict check (correct logic)
        conflict = Booking.objects.filter(
            car=car,
            start_time__lt=end_time,
            end_time__gt=start_time
        ).exclude(status='Cancelled').exists()

        if conflict:
            return render(request, 'book.html', {
                'error': '❌ Car not available at this time'
            })

        # ✅ Price calculation (20 rupees per km)
        total_price = int(round(distance * 20))

        # ✅ Save booking
        Booking.objects.create(
            name=name,
            phone=phone,
            pickup=pickup,
            drop=drop,
            start_time=start_time,
            end_time=end_time,
            car=car,
            total_price=total_price
        )

        # ✅ WhatsApp message
        message = f"""New Booking:
Name: {name}
Phone: {phone}
Pickup: {pickup}
Drop: {drop}
Distance: {distance:.2f} km
Start: {start_time}
Duration: {duration_hours} hours
Price: ₹{total_price}"""

        encoded_msg = urllib.parse.quote(message)
        whatsapp_url = f"https://wa.me/919755422892?text={encoded_msg}"

        return render(request, 'book.html', {
            'success': True,
            'whatsapp_url': whatsapp_url
        })

    return render(request, 'book.html')


def about(request):
    return render(request, 'about.html')