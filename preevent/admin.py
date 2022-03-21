from django.contrib import admin

# Register your models here.
from .models import Event, SeatBooking, TransactionDetails

admin.site.register(Event)
admin.site.register(SeatBooking)
admin.site.register(TransactionDetails)
