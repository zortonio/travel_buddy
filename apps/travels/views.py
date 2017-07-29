from django.shortcuts import render, redirect
from django.contrib import messages
from ..reg_login.models import User
from .models import Trip_Schedule

# Create your views here.
def index(req):
    if 'user_id' in req.session:
        context = {
            'user': User.objects.get(id=req.session['user_id']),
            'user_trips': Trip_Schedule.objects.filter(user_id=req.session['user_id']) | Trip_Schedule.objects.filter(joined_user_id=req.session['user_id']),
            'other_trips': Trip_Schedule.objects.all().exclude(user_id=req.session['user_id']).exclude(joined_user_id=req.session['user_id']),
        }
        return render(req, 'travels/index.html', context)
    else:
        return redirect('reg_login:index')

def logout(req):
    del req.session['user_id']
    messages.error(req, "User Logged Out")
    return redirect('reg_login:index')

def add(req):
    if 'user_id' in req.session:
        return render(req, 'travels/add.html')
    else:
        return redirect('reg_login:index')

def validate(req):
    if Trip_Schedule.objects.validate(req):
        return redirect('travels:index')
    else:
        return redirect('travels:add')

def destination(req, id):
    if 'user_id' in req.session:
        context = {
            'trip': Trip_Schedule.objects.get(id=id)
        }
        return render(req, 'travels/destination.html', context)
    else:
        return redirect('reg_login:index')

def join(req, id):
    trip = Trip_Schedule.objects.get(id=id)
    user = User.objects.get(id=req.session['user_id'])
    if user in trip.joined_user_id.all():
        return redirect('travels:index')
    else:
        trip.joined_user_id.add(user)
        return redirect('travels:index')
