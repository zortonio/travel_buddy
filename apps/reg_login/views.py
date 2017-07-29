from django.shortcuts import render, HttpResponse, redirect
from .models import User

# Create your views here.
def index(req):
    return render(req, 'reg_login/index.html')

def validate(req, route):
    if route=='register':
        if User.objects.register(req):
            return redirect('travels:index')
        else:
            return redirect('/')
    elif route=='login':
        if User.objects.login(req):
            return redirect('travels:index')
        else:
            return redirect('/')
