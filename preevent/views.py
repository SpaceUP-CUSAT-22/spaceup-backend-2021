import django_filters
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

    @action(detail=False, methods=["get"], url_path='verify', permission_classes=[permissions.IsAuthenticated])
    def verify(self, request, *args, **kwargs):
        context = {}
        if request.user.tokens.is_volunteer():
            if request.method == "POST":
                token = request.POST.get("token")
                try:
                    user = Tokens.objects.get(private_token=token).user
                    for seat in SeatBooking.objects.filter(user=user):
                        seat.verified = True
                        seat.save()
                except Tokens.DoesNotExist:
                    pass
            try:
                token = request.data.get('token')
                user = Tokens.objects.filter(private_token=token)
                SeatBooking.objects.filter(user=user)
                context['to_verify_seats'] = [seat for seat in SeatBooking.objects.filter(user=user, verified=False)]
                context['verified_seats'] = [seat for seat in SeatBooking.objects.filter(user=user, verified=True)]

            except Tokens.DoesNotExist:
                pass
            return render(request, template_name="verify.html", context=context)
        context['verified_seats'] = [seat for seat in SeatBooking.objects.filter(user=user, verified=True)]
        token = request.data.get('token')
        user = Tokens.objects.get(private_token=token).user
        seats = 0
        for seat in SeatBooking.objects.filter(user=user):
            seats += seat.seats
        context['num_seats'] = seats
        return render(request, template_name="ticket.html", context=context)


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
