import threading

from django.contrib import admin, messages

# Register your models here.
from .models import Event, SeatBooking, TransactionDetails, DataRazorpay
from home.utils import send_bulk_async_mail

admin.site.register(Event)
admin.site.register(DataRazorpay)
admin.site.register(TransactionDetails)


@admin.register(SeatBooking)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ("first_name", "phone_number", "email", 'verified')
    actions = ['send_mail', 'verify']

    @staticmethod
    def send_mail(self, _, queryset):
        threading.Thread(target=send_bulk_async_mail, args=(queryset,)).start()

    @staticmethod
    def verify(self, _, queryset):
        for seat in queryset:
            seat.verified_seats = 1
            seat.verified = True
            seat.save()
