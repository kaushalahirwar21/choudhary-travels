from django.shortcuts import render, redirect
from .models import Car, Booking
from datetime import datetime, timedelta
import urllib.parse


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

        # 🔥 Convert start time
        start_time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M")

        # 🔥 Default 2 hours booking
        end_time = start_time + timedelta(hours=2)

        car = Car.objects.first()

        # 🔥 Availability check
        conflict = Booking.objects.filter(
            car=car,
            start_time__lt=end_time,
            end_time__gt=start_time
        ).exists()

        if conflict:
            return render(request, 'book.html', {
                'error': '❌ Car not available at this time'
            })

        # 🔥 Price calculation
        duration = end_time - start_time
        hours = duration.total_seconds() / 3600
        hours = max(1, hours)

        total_price = 100 + (hours * car.price_per_hour)

        # 🔥 Save booking
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

        # 🔥 WhatsApp message
        message = f"""New Booking:
Name: {name}
Phone: {phone}
Pickup: {pickup}
Drop: {drop}
Start: {start_time}
Duration: 2 hours
Price: ₹{total_price}"""

        encoded_msg = urllib.parse.quote(message)
        whatsapp_url = f"https://wa.me/919755422892?text={encoded_msg}"

        return redirect(whatsapp_url)

    return render(request, 'book.html')


def about(request):
    return render(request, 'about.html')