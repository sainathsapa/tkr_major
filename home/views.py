from os import fdopen, name
from difflib import SequenceMatcher
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.template import *
from django.contrib.sites.shortcuts import get_current_site
from django.db import connection
# from home.form import addStudetForm
# from home.models import stdnt_Model_A  




# Create your views here.
def index(request):
    # print(request.user)
    # if request.user.is_anonymous:
    #     return redirect("/login") 
    send_Var={
            'title':'Teegala Krisha Reddy Engineering College'
        }
        
    return render(request, 'index.html', send_Var)

def dept(request):
    # print(request.user)
    # if request.user.is_anonymous:
    #     return redirect("/login") 
    send_Var={
            'title':'Teegala Krisha Reddy Engineering College'
        }
        
    return render(request, 'departments.html', send_Var)

def error_404(request, exception):
    domain = ''.join(['http://', get_current_site(request).domain])
    app_url = request.path
    context={
        'domain':domain,
        'app_url':app_url
    }

    return render(request, 'error.html', context)