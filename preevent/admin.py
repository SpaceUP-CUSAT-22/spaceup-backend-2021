from django.contrib import admin, messages

# Register your models here.
from .models import Event, SeatBooking, TransactionDetails

admin.site.register(Event)
# admin.site.register()
admin.site.register(TransactionDetails)


def generate_qr(request, queryset):
    for booking in queryset:
        booking.generate()
    messages.success(request, "QR Generated successfully")


@admin.register(SeatBooking)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ("first_name", "phone_number", "email", 'payment_status')
    actions = ['generate_qr',]
