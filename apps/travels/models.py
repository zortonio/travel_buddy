from __future__ import unicode_literals
from django.contrib import messages
from django.utils.dateparse import parse_date
from ..reg_login.models import User
from datetime import date

from django.db import models

# Create your models here.
class Trip_Schedule_Manager(models.Manager):
    def validate(self, request):
        data_to_validate = request.POST
        valid = True
        #All fields must be filled out
        if len(data_to_validate['destination'])<1 or len(data_to_validate['description'])<1 or len(data_to_validate['travel_date_from'])<1 or len(data_to_validate['travel_date_to'])<1:
            valid = False
            messages.error(request, "All fields must be filled out")
        #Travel Dates should be future dated
        try:
            if parse_date(data_to_validate['travel_date_from']) < date.today() or parse_date(data_to_validate['travel_date_to']) < date.today():
                valid = False
                messages.error(request, "All Dates must be future dated.")
        except TypeError as e:
            pass
        #Start Date must be before End Date
        try:
            if parse_date(data_to_validate['travel_date_from']) > parse_date(data_to_validate['travel_date_to']):
                valid = False
                messages.error(request, "Start Date must be before End Date")
        except TypeError as e:
            pass

        if valid:
            user = User.objects.get(id=request.session['user_id'])
            self.create(user_id=user, destination=data_to_validate['destination'], description=data_to_validate['description'], travel_start_date=data_to_validate['travel_date_from'], travel_end_date=data_to_validate['travel_date_to'])

        return valid
class Trip_Schedule(models.Model):
    user_id = models.ForeignKey(User)
    joined_user_id = models.ManyToManyField(User, related_name='joined_trips')
    destination = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    travel_start_date = models.DateField(auto_now=False, auto_now_add=False)
    travel_end_date = models.DateField(auto_now=False, auto_now_add=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Trip_Schedule_Manager()
