from django.db import models

class Car(models.Model):
    name = models.CharField(max_length=100)
    price_per_hour = models.FloatField()
    is_available = models.BooleanField(default=True)

    # 🔥 image add
    image = models.ImageField(upload_to='cars/', null=True, blank=True)

    def __str__(self):
        return self.name

class Booking(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    pickup = models.CharField(max_length=200)
    drop = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    total_price = models.FloatField()
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return self.name
    
STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Confirmed', 'Confirmed'),
    ('Cancelled', 'Cancelled'),
]

status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')    