from django.contrib import admin

# Register your models here.
from .models import Mentors, Volunteers

admin.site.register(Mentors)
admin.site.register(Volunteers)
