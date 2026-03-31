import math
import urllib.parse
from datetime import datetime, timedelta

from django.shortcuts import render, redirect
from django.utils import timezone

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
        ).exists()

        if conflict:
            return render(request, 'book.html', {
                'error': '❌ Car not available at this time'
            })

        # ✅ Price calculation
        duration = end_time - start_time
        hours = math.ceil(duration.total_seconds() / 3600)

        total_price = 100 + (hours * car.price_per_hour)

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
Start: {start_time}
Duration: {hours} hours
Price: ₹{total_price}"""

        encoded_msg = urllib.parse.quote(message)
        whatsapp_url = f"https://wa.me/919755422892?text={encoded_msg}"

        return redirect(whatsapp_url)

    return render(request, 'book.html')


def about(request):
    return render(request, 'about.html')