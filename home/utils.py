import threading
import time

from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User

from preevent.models import SeatBooking

content_new = "Greetings from SpaceUp CUSAT, Here's your ticket for successful registration for SpaceUp CUSAT 2022. Please carry your mobile phones containing your tickets for scanning at the entry. Thanks & Regards SpaceUp CUSAT 2022"

sub = "Ticket for Students' Space Summit 2022"


def get_ticket(seat: SeatBooking):
    html = """ <style>
 	body, table, td, a { -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; }
	table, td { mso-table-lspace: 0pt; mso-table-rspace: 0pt; }
	img { -ms-interpolation-mode: bicubic; }
	img { border: 0; height: auto; line-height: 100%; outline: none; text-decoration: none; }
	table { border-collapse: collapse !important; }
	body { height: 100% !important; margin: 0 !important; padding: 0 !important; width: 100% !important; }
	a[x-apple-data-detectors] { color: inherit !important; text-decoration: none !important; font-size: inherit !important; font-family: inherit !important; font-weight: inherit !important; line-height: inherit !important; }
	div[style*="margin: 16px 0;"] { margin: 0 !important; }
 	</style>
	<body style="background-color: #f7f5fa; margin: 0 !important; padding: 0 !important;">
	
		<table border="0" cellpadding="0" cellspacing="0" width="100%">
			<tr>
				<td bgcolor="#426899" align="center">
					<table border="0" cellpadding="0" cellspacing="0" width="480" >
						<tr>
							<td align="center" valign="top" style="padding: 40px 10px 40px 10px;">
								<img src=https://spaceupcusat.org/static/media/space_up-logo.5d551c8892d10d0067fd.png alt='logo'>
							</td>
						</tr>
					</table>
				</td>
			</tr>
			<tr>
				<td bgcolor="#426899" align="center" style="padding: 0px 10px 0px 10px;">
					<table border="0" cellpadding="0" cellspacing="0" width="480" >
						<tr>
							<td bgcolor="#ffffff" align="left" valign="top" style="padding: 30px 30px 20px 30px; border-radius: 4px 4px 0px 0px; color: #111111; font-family: Helvetica, Arial, sans-serif; font-size: 48px; font-weight: 400; line-height: 48px;">
								<h1 style="font-size: 32px; font-weight: 400; margin: 0;  text-align: center;">Ticket for Student's Space Summit 2022</h1>
							</td>
						</tr>
					</table>
				</td>
			</tr>
			<tr>
				<td bgcolor="#f4f4f4" align="center" style="padding: 0px 10px 0px 10px;">
					<table border="0" cellpadding="0" cellspacing="0" width="480" >
						<tr>
							<td bgcolor="#ffffff" align="left">
								<table width="100%" border="0" cellspacing="0" cellpadding="0">
                  <tr>
                    <td colspan="2" style="padding-left:30px;padding-right:15px;padding-bottom:10px; font-family: Helvetica, Arial, sans-serif; font-size: 16px; font-weight: 400; line-height: 25px;">
                      <p> <strong>Greetings from SpaceUp CUSAT</strong>,<br><br> Here's your ticket for successful registration for SpaceUp CUSAT 2022. Please carry your mobile phones containing your tickets for scanning at the entry.<br><br> Thanks & Regards <br> SpaceUp CUSAT 2022</p>
                    </td>
                  </tr>""" + f"""
									<tr>
										<th align="left" valign="top" style="padding-left:30px;padding-right:15px;padding-bottom:10px; font-family: Helvetica, Arial, sans-serif; font-size: 18px; font-weight: 400; line-height: 25px;">E-Mail</th>
										<td align="left" valign="top" style="padding-left:15px;padding-right:30px;padding-bottom:10px;font-family: Helvetica, Arial, sans-serif; font-size: 18px; font-weight: 400; line-height: 25px;">{seat.email}</td>
									</tr>
                  <tr>
										<th align="left" valign="top" style="padding-left:30px;padding-right:15px;padding-bottom:10px; font-family: Helvetica, Arial, sans-serif; font-size: 18px; font-weight: 400; line-height: 25px;">Name</th>
										<td align="left" valign="top" style="padding-left:15px;padding-right:30px;padding-bottom:10px;font-family: Helvetica, Arial, sans-serif; font-size: 18px; font-weight: 400; line-height: 25px;">{seat.first_name} {seat.second_name}</td>
									</tr>
                  <tr>
										<th align="left" valign="top" style="padding-left:30px;padding-right:15px;padding-bottom:30px; font-family: Helvetica, Arial, sans-serif; font-size: 18px; font-weight: 400; line-height: 25px;">Ticket id</th>
										<td align="left" valign="top" style="padding-left:15px;padding-right:30px;padding-bottom:30px;font-family: Helvetica, Arial, sans-serif; font-size: 18px; font-weight: 400; line-height: 25px;">{seat.transaction_id}</td>
									</tr>
								</table>
							</td>
						</tr>
						<tr>
							<td bgcolor="#ffffff" align="center">
								<table width="100%" border="0" cellspacing="0" cellpadding="0">
									<tr>
										<td bgcolor="#ffffff" align="center" style="padding: 30px 30px 30px 30px; border-top:1px solid #dddddd;">
											<table border="0" cellspacing="0" cellpadding="0">
												<tr>
													<td align="left" style="border-radius: 3px;" bgcolor="#426899">
														<a href="{seat.get_url()}" target="_blank" style="font-size: 20px; font-family: Helvetica, Arial, sans-serif; color: #ffffff; text-decoration: none; color: #ffffff; text-decoration: none; padding: 11px 22px; border-radius: 2px; border: 1px solid #426899; display: inline-block;">Download</a>
													</td>
												</tr>
											</table>
										</td>
									</tr>
								</table>
							</td>
						</tr>
					</table>
				</td>
			</tr>
			<tr>
				<td bgcolor="#f4f4f4" align="center" style="padding: 0px 10px 0px 10px;"> <table border="0" cellpadding="0" cellspacing="0" width="480">
					<tr>
						<td bgcolor="#f4f4f4" align="left" style="padding: 30px 30px 30px 30px; color: #666666; font-family: Helvetica, Arial, sans-serif; font-size: 14px; font-weight: 400; line-height: 18px;" >
							<a href="spaceupcusat.org" style="margin: 0;">spaceupcusat.org</a>
						</td>
					</tr>
				</td>
			</tr>
		</table>
	
	</body>"""
    return html


class EmailThread(threading.Thread):
    def __init__(self, subject, content, recipient_list, ticket):
        self.subject = subject
        self.ticket = ticket
        self.recipient_list = recipient_list
        self.content = content
        threading.Thread.__init__(self)

    def run(self):
        send_mail(self.subject, content_new, settings.EMAIL_HOST_USER, self.recipient_list,
                  html_message=get_ticket(self.ticket),
                  fail_silently=False, )
        print(f'Mail [{self.subject}] sent to {self.recipient_list}')


# def send_async_mail(subject=sub, content=content_new, recipient_list=None):
#     if recipient_list is None:
#         recipient_list = ['sunithvazhenkada@gmail.com', ]
#     EmailThread(subject, content, recipient_list).start()


class BulkEmail(threading.Thread):
    def __init__(self, objects):
        self.objects = objects
        threading.Thread.__init__(self)

    def run(self):
        count = 0
        for i in self.objects:
            thre = EmailThread(sub, content_new, [i.email], i)
            thre.start()
            thre.join()
            time.sleep(10)
            if count > 50:
                time.sleep(200)
                count = 0
            count += 1
            print(f'Mail to all')


def send_bulk_async_mail(seats):
    BulkEmail(seats).start()

