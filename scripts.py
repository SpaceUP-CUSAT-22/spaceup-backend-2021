from pandas import read_excel
from preevent.models import SeatBooking


def create():
    # SeatBooking.objects.all().delete()
    sheet = read_excel(open("payment.xlsx", 'rb'))
    print(sheet)
    count = 0
    for record in sheet.values:
        if record[10] == "captured":
            print(record[10])
            seat, _ = SeatBooking.objects.get_or_create(payment_status=True, first_name=record[12],
                                                        cusatian=(record[17] == "Yes"),
                                                        seds_member=(record[16] == "Yes"),
                                                        phone_number=record[14], email=record[13],
                                                        institution=record[15],
                                                        vegetarian=(record[18] == "Yes"), payment_id=record[11],
                                                        amount=record[5])

    print(count)

# create()
