import urllib.parse
from datetime import datetime, timedelta

from django.shortcuts import render
from django.utils import timezone

from geopy.distance import geodesic
from geopy.geocoders import Nominatim

from .models import Booking, Car


def home(request):
    return render(request, 'home.html')


def book(request):
    context = {
        'form_data': {
            'name': '',
            'phone': '',
            'pickup': '',
            'drop': '',
            'start_time': '',
            'hours': '2',
        }
    }

    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        pickup = request.POST.get('pickup')
        drop = request.POST.get('drop')
        start_time_raw = request.POST.get('start_time')
        hours = request.POST.get('hours', '2')

        context['form_data'] = {
            'name': name or '',
            'phone': phone or '',
            'pickup': pickup or '',
            'drop': drop or '',
            'start_time': start_time_raw or '',
            'hours': hours or '2',
        }

        if not name or not phone or not pickup or not drop or not start_time_raw:
            context['error'] = 'All fields fill karna zaroori hai.'
            return render(request, 'book.html', context)

        try:
            duration_hours = int(hours)
        except (TypeError, ValueError):
            context['error'] = 'Trip duration valid number me dalo.'
            return render(request, 'book.html', context)

        if duration_hours < 1 or duration_hours > 24:
            context['error'] = 'Trip duration 1 se 24 ghante ke beech honi chahiye.'
            return render(request, 'book.html', context)

        try:
            start_time = datetime.strptime(start_time_raw, "%Y-%m-%dT%H:%M")
            start_time = timezone.make_aware(start_time)
        except ValueError:
            context['error'] = 'Start time sahi format me select karo.'
            return render(request, 'book.html', context)

        if start_time < timezone.now():
            context['error'] = 'Past time ke liye booking nahi ho sakti.'
            return render(request, 'book.html', context)

        end_time = start_time + timedelta(hours=duration_hours)

        geolocator = Nominatim(user_agent="choudhary_travels")
        try:
            pickup_location = geolocator.geocode(pickup)
            drop_location = geolocator.geocode(drop)
            if not pickup_location or not drop_location:
                context['error'] = 'Pickup ya drop location nahi mili. Thoda detailed address dalo.'
                return render(request, 'book.html', context)
            distance = geodesic(
                (pickup_location.latitude, pickup_location.longitude),
                (drop_location.latitude, drop_location.longitude),
            ).km
        except Exception:
            context['error'] = 'Distance calculate nahi ho paayi. Thodi der baad dobara try karo.'
            return render(request, 'book.html', context)

        car = Car.objects.filter(is_available=True).first()
        if not car:
            context['error'] = 'Abhi koi car available nahi hai.'
            return render(request, 'book.html', context)

        conflict = Booking.objects.filter(
            car=car,
            start_time__lt=end_time,
            end_time__gt=start_time,
        ).exclude(status='Cancelled').exists()

        if conflict:
            context['error'] = 'Is time slot me car available nahi hai.'
            return render(request, 'book.html', context)

        total_price = int(round(distance * 20))

        Booking.objects.create(
            name=name,
            phone=phone,
            pickup=pickup,
            drop=drop,
            start_time=start_time,
            end_time=end_time,
            car=car,
            total_price=total_price,
        )

        message = f"""New Booking:
Name: {name}
Phone: {phone}
Pickup: {pickup}
Drop: {drop}
Distance: {distance:.2f} km
Start: {start_time}
Duration: {duration_hours} hours
Price: Rs. {total_price}"""

        encoded_msg = urllib.parse.quote(message)
        whatsapp_url = f"https://wa.me/919755422892?text={encoded_msg}"

        return render(request, 'book.html', {
            'success': True,
            'whatsapp_url': whatsapp_url,
            'booking_summary': {
                'car': car.name,
                'distance': f"{distance:.2f}",
                'price': total_price,
                'hours': duration_hours,
            },
        })

    return render(request, 'book.html', context)


def about(request):
    return render(request, 'about.html')
