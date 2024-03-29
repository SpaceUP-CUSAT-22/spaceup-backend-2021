import django_filters
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
# from django.shortcuts import render
from django.shortcuts import render
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
import logging

from config import settings
from .models import Event, SeatBooking, Question
from .serializers import GetEventSerializer, GetSeatBookingSerializer, QuestionsSerializer
from .utils import cancel_last_payment_links, get_payment_link, verify_signature, handle_payment
from authentication.models import Tokens

logger = logging.getLogger('home')


class EventViewSet(viewsets.ModelViewSet):
    """
    API end point to get all product details
    """
    http_method_names = ['get']
    queryset = Event.objects.all()
    serializer_class = GetEventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, django_filters.rest_framework.DjangoFilterBackend]
    search_fields = ['title', 'description', 'venue', 'hall_name']


class SeatBookingViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post']
    queryset = SeatBooking.objects.all()
    serializer_class = GetSeatBookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SeatBooking.objects.filter(user=self.request.user, payment_status=True)

    @action(detail=False, methods=["post"], url_path='book')
    def book(self, request, *args, **kwargs):
        cancel_last_payment_links(request.user)
        logger.info(request.data)
        seats = request.data['seats']
        event = request.data['event']
        logger.info(seats)
        try:
            event = Event.objects.get(id=event)
        except Event.DoesNotExist:
            event = Event.objects.all().first()

        if type(seats) == type(1) and seats > 0:
            amount = event.booking_price * seats
            payment_url, transaction_details = get_payment_link(request.user, amount, seats, event)
            if payment_url:
                return Response({"payment_url": payment_url})
            return Response({"detail": "error anh monuse"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response({"detail": "selected_seats must be a number greater than 0"},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

    # TODO make this for vol
    @action(detail=False, methods=["get", "post"], url_path='verify',
            permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    def verify(self, request, *args, **kwargs):
        if request.method == "POST":
            if request.user.is_authenticated and request.user.tokens.is_volunteer():
                ticket_id = request.GET['ticket']
                seat = SeatBooking.objects.get(transaction_id=ticket_id)
                if seat.verified_seats < seat.seats:
                    seat.verified_seats += 1
                    seat.verified = True
                seat.save()
        context = {}

        ticket_id = request.GET['ticket']
        try:
            seat = SeatBooking.objects.get(transaction_id=ticket_id)
            context = {

                "seat_booking": seat,
            }
        except SeatBooking.DoesNotExist:
            context['errr'] = "Invalid ticket"
        if request.user.is_authenticated and request.user.tokens.is_volunteer():
            return render(request, template_name="dashboard_profile.html", context=context)
        return render(request, template_name="dashboard_tickets.html", context=context)

        # if request.method == "get":
        #
        #
        # else:
        #     if request.user.tokens.is_volunteer():
        #         ticket_id = request.post['ticket']
        #         seat = SeatBooking.objects.get(transaction_id=ticket_id)
        #         seat.verified = True
        #         seat.save()


@login_required
def book_seats(request):
    context1 = {}
    if request.method == "POST":
        event = Event.objects.filter().first()
        first_name = request.POST.get('first_name')
        second_name = request.POST.get('second_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        seats = 1
        institution = request.POST.get('institution')
        vegetarian = request.POST.get('vegetarian')
        print(f'{vegetarian =}')
        SeatBooking.objects.create(user=request.user, first_name=first_name, second_name=second_name, email=email,
                                   phone_number=phone_number, seats=seats, institution=institution,
                                   vegetarian=True if vegetarian == "on" else False)
        print(f'{seats = }')
        if int(seats) > 0:
            payment_url, transaction_details = get_payment_link(request.user, int(seats) * event.booking_price,
                                                                int(seats), event)
            return HttpResponseRedirect(payment_url)
    return render(request, template_name="seat_booking.html", context=context1)


@api_view(["GET"])
def payment(request):
    print(request)
    logger.info("Webhook from razorpay called ...")
    if verify_signature(request):
        transaction_id = request.GET["razorpay_payment_link_reference_id"]
        payment_status = request.GET["razorpay_payment_link_status"]
        handle_payment(transaction_id, payment_status)
    else:
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
    return HttpResponseRedirect(settings.webhook_redirect_url)


class QuestionViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post']
    queryset = Question.objects.all()
    serializer_class = QuestionsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff():
            return Question.objects.all()
        return Question.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
