import django_filters
from django.http import HttpResponseRedirect
# from django.shortcuts import render
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
import logging

from config import settings
from .models import Event, SeatBooking
from .serializers import GetEventSerializer, GetSeatBookingSerializer
from .utils import cancel_last_payment_links, get_payment_link, check_available_seats, verify_signature, handle_payment

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
        seats = request.data['selected_seats']
        logger.info(seats)
        event = Event.objects.all().first()
        seat, available = check_available_seats(event, seats)
        if not available:
            return Response({"detail": f"requested seat {seat} not available please book another"})
        logger.info('seats are available')
        amount = event.booking_price * len(seats)
        payment_url, transaction_details = get_payment_link(request.user, amount, seats)
        if payment_url:
            return Response({"payment_url": payment_url})
        return Response({"detail": "error anh monuse"})


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
