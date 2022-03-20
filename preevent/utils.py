import hashlib
import hmac
import logging

import requests
from requests.auth import HTTPBasicAuth

from config import settings
from preevent.models import TransactionDetails, Event, SeatBooking

logger = logging.getLogger('home')


def cancel_last_payment_links(user):
    logger.info("Cancelling last payment links")
    transaction_details = TransactionDetails.objects.filter(user=user, payment_status="created")
    key_secret = settings.razorpay_key_secret
    key_id = settings.razorpay_key_id
    for transaction in transaction_details:
        url = f'https://api.razorpay.com/v1/payment_links/{transaction.payment_id}/cancel'
        logger.info(f"canceling  {transaction.payment_id}")
        requests.post(url,
                      headers={'Content-type': 'application/json'},
                      auth=HTTPBasicAuth(key_id, key_secret))
        transaction.delete()


def get_payment_link(user, amount, seats):
    """
    This Function returns thr payment url for that particular checkout
    Returns a list with payment link and payment id created by razorpay
    """
    logger.info(f"{user} Requesting to get payment link ")
    key_secret = settings.razorpay_key_secret
    call_back_url = settings.webhook_call_back_url
    key_id = settings.razorpay_key_id
    cancel_last_payment_links(user)

    transaction_details = TransactionDetails(user=user,
                                             total=amount, seat_numbers=seats)
    transaction_details.save()
    logger.info(f"created transaction details object for {user}")
    amount *= 100
    amount = int(amount)
    try:
        url = 'https://api.razorpay.com/v1/payment_links'

        data = {
            "amount": amount,
            "currency": "INR",
            "callback_url": call_back_url,
            "callback_method": "get",
            'reference_id': transaction_details.transaction_id,
            "customer": {
                "contact": user.tokens.mobile_number,
                "email": user.email,
                "name": f"{user.firstname} {user.lastname}"
            },
            "options": {
                "checkout": {
                    "name": "DreamEat",
                    "prefill": {
                        "email": user.email,
                        "contact": user.tokens.mobile_number
                    },
                    "readonly": {
                        "email": True,
                        "contact": True
                    }
                }
            }
        }
        x = requests.post(url,
                          json=data,
                          headers={'Content-type': 'application/json'},
                          auth=HTTPBasicAuth(key_id, key_secret))
        res = x.json()
        try:
            logger.info(f"Razorpay response object {res} ")
            transaction_details.payment_id = res.get("id")
            logger.info(f" Transaction id {res.get('id')} ,  status = {res.get('status')}")
            transaction_details.payment_status = res.get("status")
            transaction_details.save()
            logger.info(f"now created transaction details is {transaction_details}")
            payment_url = res.get('short_url')
            logger.info(f"payment url - {payment_url}")
            return [payment_url, transaction_details]
        except KeyError:
            logger.warning(f"payment link creation failed ... {res} ")
            return [False, False]
    except Exception as e:
        logger.warning(e)
        return [False, False]


def check_available_seats(event: Event, seats):
    for seat in seats:
        if seat not in event.available_seats:
            return seat, False
    return True, True


def verify_signature(request):
    logger.info("Signature verification taking place")
    try:
        signature_payload = request.GET['razorpay_payment_link_id'] + '|' + \
                            request.GET['razorpay_payment_link_reference_id'] + '|' + \
                            request.GET['razorpay_payment_link_status'] + '|' + \
                            request.GET['razorpay_payment_id']
        signature_payload = bytes(signature_payload, 'utf-8')
        byte_key = bytes(settings.razorpay_key_secret, 'utf-8')
        generated_signature = hmac.new(byte_key, signature_payload, hashlib.sha256).hexdigest()
        if generated_signature == request.GET["razorpay_signature"]:
            logger.info("Signature verification successfully completed")
            return True
        else:
            logger.warning("signature verification failed")
            return False
    except ValueError:
        logger.warning("signature verification failed value error")
        return False
    except Exception as e:
        logger.warning("signature verification failed")
        logger.warning(e)


def handle_payment(transaction_id, payment_status):
    try:
        logger.info(transaction_id)
        transaction_details = TransactionDetails.objects.get(transaction_id=transaction_id)
        transaction_details.payment_status = payment_status
        logger.info(f"payment status {transaction_details.payment_status}")
        transaction_details.save()

        for seat in transaction_details.seat_numbers:
            SeatBooking.objects.create(user=transaction_details.user, payment_status=True,
                                       seat_number=seat,
                                       event=transaction_details.event)
            transaction_details.event.booked_seats.append(seat)

    except Exception as ex:
        logger.critical(f"order not created exception {ex} ")
