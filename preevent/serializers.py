from rest_framework import serializers

from .models import Event, SeatBooking, Question


class GetEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'title', 'type', 'description', 'venue',
            'venue_location', 'mentors', 'volunteers',
            'poster', 'seat_booking_status',
        ]


class GetSeatBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeatBooking
        fields = ['event', 'seats', 'payment_status','verified']

        extra_kwargs = {
            'payment_status': {'read_only': True},
            'verified': {'read_only': True},
        }


class QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['user', 'question']

        extra_kwargs = {
            'user': {'read_only': True},
        }
