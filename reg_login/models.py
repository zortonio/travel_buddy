from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import re
import bcrypt

VALID_EMAIL = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
ALL_LETTERS = re.compile(r'^[a-zA-Z\s]+$')
# Create your models here.
class UserManager(models.Manager):
    def register(self, request):
        data_to_validate = request.POST
        valid = True
        #All Fields are filled out
        if len(data_to_validate['name'])<1 or len(data_to_validate['username'])<1 or len(data_to_validate['email'])<1 or len(data_to_validate['pw'])<1 or len(data_to_validate['pw_confirm'])<1:
            valid = False
            messages.error(request, "All fields are required.")
        #Name is all letters
        if not ALL_LETTERS.match(data_to_validate['name']):
            valid = False
            messages.error(request, "Name must be all letters.")
        #Username not already in use
        if len(self.filter(username=data_to_validate['username']))>0:
            valid = False
            messages.error(request, "Username is unavailable.")
        #Valid Email
        if not VALID_EMAIL.match(data_to_validate['email']):
            valid = False
            messages.error(request, "Invalid Email")
        #Password must be at least 8 characters
        if len(data_to_validate['pw']) < 8:
            valid = False
            messages.error(request, "Password must be at least 8 characters long.")
        #Passwords must match
        if not data_to_validate['pw'] == data_to_validate['pw_confirm']:
            valid = False
            messages.error(request, "Passwords must match.")

        if valid:
            en_pw = bcrypt.hashpw(data_to_validate['pw'].encode(), bcrypt.gensalt())
            self.create(
                name = data_to_validate['name'],
                username = data_to_validate['username'],
                email = data_to_validate['email'],
                password = en_pw
            )
        return valid

    def login(self, request):
        data_to_validate = request.POST
        valid = True
        #All fields are filled out
        if len(data_to_validate['username'])<1 or len(data_to_validate['pw'])<1:
            valid = False
            messages.error(request, "All field are required")
        #Check Username
        if len(self.filter(username=data_to_validate['username'])) < 1:
            valid = False
            messages.error(request, "Invalid Username")
        else:
            user_pw = self.get(username=data_to_validate['username']).password
            en_pw = bcrypt.hashpw(data_to_validate['pw'].encode(), user_pw.encode())
            if not en_pw == user_pw:
                valid = False
                message.error(request, "Invalid Password")
        return valid

class User(models.Model):
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return self.name;
