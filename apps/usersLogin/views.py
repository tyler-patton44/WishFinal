from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from time import gmtime, strftime
from django.utils.crypto import get_random_string
import random
import bcrypt
from .models import *
from ..wishList.models import *

def index(request):
    if 'first_name' not in request.session:
        request.session['first_name'] = ""
    if 'last_name' not in request.session:
        request.session['last_name'] = ""
    if 'email' not in request.session:
        request.session['email'] = ""
    if 'email2' not in request.session:
        request.session['email2'] = ""
    return render(request, 'usersLogin/index.html')

def create(request):
    if request.method == "POST":
        request.session['first_name'] = request.POST['first_name']
        request.session['last_name'] = request.POST['last_name']
        request.session['email'] = request.POST['email']

        errors = User.objects.reg_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            User.objects.insertUser(request.POST)
            
            return redirect('/')

    else:
        return redirect('/')

def login(request):
    if 'email_checker' not in request.session:
        request.session['email_checker'] = ""
    request.session['email2'] = request.POST['email2']
    wrong = User.objects.login_validator(request.POST)
    if len(wrong):
        for key, value in wrong.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['email2'])
        request.session['email_checker'] = user.email_hash
        request.session['id'] = user.id
        return redirect('/wishes')