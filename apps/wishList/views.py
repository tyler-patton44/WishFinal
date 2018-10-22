from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from time import gmtime, strftime
from django.utils.crypto import get_random_string
import random
import bcrypt
from .models import *
from ..usersLogin.models import *

def index(request):
    if 'email_checker' not in request.session:
        return redirect('/')
    context = {
        'logged': User.objects.get(email_hash=request.session['email_checker']),
        'all_dreams': Wish.objects.all()
    }
    return render(request, 'wishList/index.html', context)

def status(request):
    if 'email_checker' not in request.session:
        return redirect('/')
    context = {
        'logged': User.objects.get(email_hash=request.session['email_checker']),
        'granted_wishes': Wish.objects.filter(status='granted', user=User.objects.get(email_hash=request.session['email_checker'])),
        'pending_wishes': Wish.objects.filter(status='pending', user=User.objects.get(email_hash=request.session['email_checker'])),
        'all_dreams': Wish.objects.filter(status='granted')
    }
    print(Wish.objects.filter(status='granted'))
    return render(request, 'wishList/status.html', context)

def addWish(request):
    if 'email_checker' not in request.session:
        return redirect('/')
    context = {
        'logged': User.objects.get(email_hash=request.session['email_checker']),
    }
    return render(request, 'wishList/makeWish.html', context)

def add(request):
    if request.method == 'POST':
        if 'email_checker' not in request.session:
            return redirect('/')
        if 'wish' not in request.session:
            request.session['wish'] = ""
        if 'desc' not in request.session:
            request.session['desc'] = ""
        request.session['wish'] = request.POST['wish']
        request.session['desc'] = request.POST['desc']

        errors = Wish.objects.wishVal(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/addWish')
        else:
            Wish.objects.insertWish(request.POST)
            return redirect('/wishes')

    else:
        return redirect('/')

def editWish(request, id):
    if 'email_checker' not in request.session:
        return redirect('/')
    context = {
        'logged': User.objects.get(email_hash=request.session['email_checker']),
        'dream': Wish.objects.get(id=id)
    }
    return render(request, 'wishList/editWish.html', context)

def edit(request):
    if request.method == 'POST':
        if 'email_checker' not in request.session:
            return redirect('/')

        errors = Wish.objects.wishVal(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/EditWish')
        else:
            b = Wish.objects.get(id=int(request.POST['id']))
            b.item = request.POST['wish']
            b.desc = request.POST['desc']
            b.save()
            return redirect('/wishes')

    else:
        return redirect('/')

def deletor(request, id):
    if 'email_checker' not in request.session:
        return redirect('/')
    
    b = Wish.objects.get(id=id)
    b.delete()
    return redirect('/wishes')

def grant(request, id):
    if 'email_checker' not in request.session:
        return redirect('/')

    b = Wish.objects.get(id=id)
    b.status = 'granted'
    b.save()
    return redirect('/wishes')

def like(request, id):
    if 'email_checker' not in request.session:
        return redirect('/')
    x = User.objects.get(email_hash = request.session['email_checker'])
    results = Wish.objects.get(id=id)
    results.likes.add(x)
    results.save()
    return redirect('/wishes')
    

def logout(request):
    request.session.clear()
    return redirect('/')