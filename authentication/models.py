from billiard.five import string
from django.db import models
from django.contrib.auth.models import User
import random


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def create_new_id():
    not_unique = True
    unique_id = id_generator()
    while not_unique:
        unique_id = id_generator()
        if not Tokens.objects.filter(private_token=unique_id):
            not_unique = False
    return str(unique_id)


class Tokens(models.Model):
    private_token = models.CharField(max_length=10, unique=True, default=create_new_id)
    user = models.OneToOneField(User, related_name='tokens', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=12, default="")
    profile = models.ImageField(upload_to='images', blank=True, null=True)

    def __str__(self):
        return f"{self.user} "
