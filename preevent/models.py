import random
import string

from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator
from django.db import models

from home.models import Mentors, Volunteers
from django.contrib.auth.models import User

event_types = (
    ("Game", "Game"),
    ("Lecture", "Lecture"),
    ("Discussion", "Discussion"),
    ("Debate", "Debate")
)


class Event(models.Model):
    title = models.CharField(max_length=25)
    type = models.CharField(max_length=20, choices=event_types)
    description = models.TextField()
    venue = models.CharField(help_text='venue name', max_length=30)
    venue_location = models.CharField(max_length=150, help_text="full location link")
    mentors = models.ManyToManyField(Mentors)
    volunteers = models.ManyToManyField(Volunteers)
    poster = models.ImageField(upload_to='images/', null=True, blank=True)
    hall_name = models.CharField(max_length=20)
    seat_booking_status = models.BooleanField(default=False)
    booking_price = models.FloatField(validators=[MinValueValidator(0)])
    total_seats = models.PositiveIntegerField(default=100)

    def __str__(self):
        return self.title


class SeatBooking(models.Model):
    user = models.ForeignKey(User, related_name='booking', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, blank=True, null=True)
    payment_status = models.BooleanField(default=False)
    seats = models.PositiveIntegerField(default=1)


def code_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def create_new_transaction_id():
    not_unique = True
    unique_code = code_generator()
    while not_unique:
        unique_code = code_generator()
        if not TransactionDetails.objects.filter(transaction_id=unique_code):
            not_unique = False
    return str(unique_code)


class TransactionDetails(models.Model):
    seat_booking = models.ForeignKey(SeatBooking, related_name="transaction",
                                     on_delete=models.SET_NULL, blank=True,
                                     null=True)
    total = models.FloatField(default=0)
    # to store the random generated unique id
    transaction_id = models.CharField(max_length=10, default=create_new_transaction_id)
    user = models.ForeignKey(User, related_name="transaction", on_delete=models.CASCADE)
    # to store the id returned when creating a payment link
    payment_id = models.CharField(max_length=20, default="")
    payment_status = models.CharField(max_length=20, default="failed")
    date = models.DateField(auto_now=True, blank=True, null=True)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, blank=True, null=True)
    seats = models.PositiveIntegerField(default=0)
