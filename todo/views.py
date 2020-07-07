from django.shortcuts import render , redirect , get_object_or_404
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login , logout , authenticate
from .forms import TodoForm
from .models import Todo
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy 
from django.views.decorators.csrf import csrf_exempt
from todo.paytm import Checksum 
from django.http import HttpResponse
import json
import requests
import cgi

# Create your views here.

MERCHANT_KEY = 'nBu0n8p0lj8VMhT6'

def home(request):
    return render(request, 'todo/home.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'todo/signupuser.html', {'form':UserCreationForm()})

    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('currenttodos')

            except IntegrityError:
                return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'Username is already taken. Please choose a new username'})
        else:
            return render(request, 'todo/signupuser.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo/loginuser.html', {'form':AuthenticationForm()})

    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'] )
        if user is None:
            return render(request, 'todo/loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('currenttodos')


def FacebookAuth(request):
    return render(request, 'todo/facebook.html')
    


@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {'from':TodoForm()})

    else:
        try:
            form = TodoForm(request.POST)
            
            newtodo = form.save(commit = False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form':TodoForm(), 'error':'Bad data passed in. Try again.'})


@login_required
def currenttodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'todo/currenttodos.html', {'todos':todos})

@login_required
def completedtodos(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    
  



    return render(request, 'todo/completedtodos.html', {'todos':todos})  

    
@login_required
def viewtodo(request, todo_pk):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form = TodoForm(instance=todo)
        return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form})
        

        

           



    else:
        try:
                form = TodoForm(request.POST, instance=todo)
                
                form.save()
                return render(request, 'todo/currenttodos.html', {'todos':todos})
        except ValueError:
                return render(request, 'todo/viewtodo.html', {'todo':todo, 'form':form, 'error':'Bad Info.'})

                 

@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.datecompleted = timezone.now()
        todo.save()
        return redirect('currenttodos')

@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')


def Checkout(request, todo_pk):
         
         todo = get_object_or_404(Todo, pk=todo_pk, user=request.user)
         paytmParams = {

	
	"MID" : "RyewUB79976598377116",

	
	"WEBSITE" : "WEBSTAGING",

	
	"INDUSTRY_TYPE_ID" : "Retail",

	
	"CHANNEL_ID" : "WEB",

	"ORDER_ID" : str(todo.pk),

	
    "CUST_ID" : str(todo.user),

	
	"MOBILE_NO" : "9999999999",

	"EMAIL" : "mrigendramait2@gmail.com",

	
	"TXN_AMOUNT" : "10.00",

	
	"CALLBACK_URL" : "http://127.0.0.1:8000/Payment/",
        }
         paytmParams['CHECKSUMHASH'] = Checksum.generate_checksum(paytmParams, MERCHANT_KEY)
         return render(request, 'todo/paytm.html', {'paytmParams': paytmParams})


@csrf_exempt
def PaytmRequest(request):

    # paytm will send  you post request here

    form = request.POST
    response_dict = {}

    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY , checksum)
    if verify :
        if response_dict['RESPCODE']== '01':
            print('Order Successful')

        else:
            print("order was not Successful because" + response_dict['RESPMSG'])

    return render(request, 'todo/paytm2.html' , {'response_dict':response_dict} )