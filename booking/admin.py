from django.contrib import admin
from .models import Car, Booking

# 🔥 Admin panel branding
admin.site.site_header = "Choudhary Travels Admin"
admin.site.site_title = "Admin Panel"
admin.site.index_title = "Welcome to Dashboard"


# 🔥 Car Admin (upgrade)
class CarAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_per_hour', 'is_available', 'image_preview')
    list_filter = ('is_available',)
    search_fields = ('name',)
    list_editable = ('price_per_hour', 'is_available')

    # 🔥 image preview in admin
    def image_preview(self, obj):
        if obj.image:
            return f"<img src='{obj.image.url}' width='50' height='50' />"
        return "No Image"
    
    image_preview.allow_tags = True
    image_preview.short_description = "Image"


# 🔥 Booking Admin (upgrade)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'phone', 'pickup', 'drop',
        'start_time', 'end_time',
        'car', 'total_price', 'status'
    )
    list_filter = ('status', 'car', 'start_time')
    search_fields = ('name', 'phone', 'pickup', 'drop')

    # 🔥 important fields readonly (owner galti se change na kare)
    readonly_fields = ('total_price',)

    # 🔥 ordering latest first
    ordering = ('-start_time',)

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('<int:booking_id>/mark_confirmed/', self.admin_site.admin_view(self.mark_confirmed), name='booking_mark_confirmed'),
            path('<int:booking_id>/delete_booking/', self.admin_site.admin_view(self.delete_booking_view), name='booking_delete_booking'),
        ]
        return custom_urls + urls

    def mark_confirmed(self, request, booking_id):
        from django.shortcuts import redirect
        b = Booking.objects.get(id=booking_id)
        b.status = 'Confirmed'
        b.save()
        return redirect('admin:index')

    def delete_booking_view(self, request, booking_id):
        from django.shortcuts import redirect
        Booking.objects.filter(id=booking_id).delete()
        return redirect('admin:index')


# 🔥 Register models
admin.site.register(Car, CarAdmin)
admin.site.register(Booking, BookingAdmin)