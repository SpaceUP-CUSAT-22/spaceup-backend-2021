from rest_framework import serializers

from .models import Event, SeatBooking


class GetEventSerializer(serializers.ModelSerializer):
    available_seats = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'title', 'type', 'description', 'venue',
            'venue_location', 'mentors', 'volunteers',
            'poster', 'seat_booking_status', 'available_seats'
        ]

    @staticmethod
    def get_available_seats(event):
        return event.available_seats


class GetSeatBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeatBooking
        fields = ['event', 'seat_number', 'payment_status']

