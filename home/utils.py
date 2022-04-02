import threading
import time

from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User

html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <meta name="x-apple-disable-message-reformatting">
    <title>Minglikko.com</title>

    <style>
        table, td, div, h1, p {
            font-family: Poppins;
        }
    </style>
</head>
<body style="margin:0;padding:0;">
<table role="presentation" style="width:100%;border-collapse:collapse;border:0;border-spacing:0;background:#ffffff;">
    <tr>
        <td align="center" style="padding:0;">
            <table role="presentation"
                   style="width:602px;border-collapse:collapse;border:1px solid #cccccc;border-spacing:0;text-align:left;">
                <tr>
                    <td align="center" style="background:#F7924A;">
                        <img src="https://raw.githubusercontent.com/sunithvs/minglikko/main/static/img/final.jpeg"
                             alt="" width="100%"
                             style="height:auto;display:block;"/>
                    </td>
                </tr>
                <tr>
                    <td style="padding:36px 30px 42px 30px;">
                        <table role="presentation"
                               style="width:100%;border-collapse:collapse;border:0;border-spacing:0;">
                            <tr>
                                <td style="padding:0 0 36px 0;color:#153643;">
                                    <h1 style="color:#F7924A;font-size:24px;margin:0 0 20px 0;font-family:Arial,sans-serif;">
                                        Congrats 🎉🎉, you've found your perfect match !</h1>
                                    <p style="margin:0 0 12px 0;font-size:16px;line-height:24px;font-family:Arial,sans-serif;">
                                        Dear Human Being<br/>
                                    Thanks for your lively participation. Hope you enjoyed the game. We'll be back with even more exciting events soon ;)
                                    </p>
                                    <p style="margin:0;font-size:16px;line-height:24px;font-family:Arial,sans-serif;">

                                        <br/>
                                        <a href="http://minglikko.com"
                                           style="color:#F7924A;text-decoration:underline;"> Chat here</a>


                                    </p>

                                </td>
                            </tr>

                        </table>
                    </td>
                </tr>
                <tr>
                    <td style="padding:30px;background:#F7924A;">
                        <table role="presentation"
                               style="width:100%;border-collapse:collapse;border:0;border-spacing:0;font-size:9px;font-family:Arial,sans-serif;">
                            <tr>
                                <td style="padding:0;width:50%;" align="left">
                                    <p style="margin:0;font-size:14px;line-height:16px;font-family:Arial,sans-serif;color:#ffffff;">
                                        Regards
                                        Team Minglikko<br/><a href="http://minglikko.com"
                                                              style="color:#ffffff;text-decoration:underline;">minglikko.com</a>
                                    </p>
                                </td>
                                <td style="padding:0;width:50%;" align="right">
                                    <table role="presentation"
                                           style="border-collapse:collapse;border:0;border-spacing:0;">
                                        <tr>
                                            <td style="padding:0 0 0 10px;width:38px;">
                                                <a href="http://minglikko.com/" style="color:#ffffff;"><img
                                                        src="https://assets.codepen.io/210284/tw_1.png" alt="Twitter"
                                                        width="38" style="height:auto;display:block;border:0;"/></a>
                                            </td>
                                            <td style="padding:0 0 0 10px;width:38px;">
                                                <a href="http://minglikko.com/" style="color:#ffffff;"><img
                                                        src="https://assets.codepen.io/210284/fb_1.png" alt="Facebook"
                                                        width="38" style="height:auto;display:block;border:0;"/></a>
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
</table>
</body>
</html>
"""
content_new = """ Thanks for your lively participation. Hope you enjoyed the game. We'll be back with even more exciting events soon ;)"""

sub = "Minglikko Partner waiting for your message"


class EmailThread(threading.Thread):
    def __init__(self, subject, content, recipient_list):
        self.subject = subject
        self.recipient_list = recipient_list
        self.content = content
        threading.Thread.__init__(self)

    def run(self):
        send_mail(self.subject, content_new, settings.EMAIL_HOST_USER, self.recipient_list, html_message=html,
                  fail_silently=False, )
        print(f'Mail [{self.subject}] sent to {self.recipient_list}')


def send_async_mail(subject=sub, content=content_new, recipient_list=None):
    if recipient_list is None:
        recipient_list = ['sunithvazhenkada@gmail.com', ]
    # print(content)
    EmailThread(subject, content, recipient_list).start()


class BulkEmail(threading.Thread):
    def __init__(self, objects):
        self.objects = objects
        threading.Thread.__init__(self)

    def run(self):
        count = 0
        for i in self.objects:
            # print(i[1])
            thre = EmailThread(sub, content_new, [i.email])
            thre.start()
            thre.join()
            time.sleep(3)
            if count > 50:
                time.sleep(200)
                count = 0
            count += 1
            print(f'Mail to all')


def send_bulk_async_mail():
    users = User.objects.exclude(tokens__chat_friends=None)
    # print(len(users))
    BulkEmail(users).start()


send_bulk_async_mail()
