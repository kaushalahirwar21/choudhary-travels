from django import template
from booking.models import Booking

register = template.Library()

@register.simple_tag
def get_recent_bookings():
    return Booking.objects.exclude(status='Cancelled').order_by('-start_time')[:10]
