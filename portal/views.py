import os
from django.conf import settings

from django.http.response import Http404
from portal.models import Assignments, Students_Model, Teachers_Model, Assignemnt_Submissions
from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.template import *
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, FormView
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django import template

register = template.Library()

@register.filter
def get_type(value):
    return type(value)




def process(request):

    if request.session.get('UserName'):
        return HttpResponseRedirect('teach_dashboard')
    if request.session.get('stdnt_usr'):
        return HttpResponseRedirect('stdnt_dash')
    else:
        return HttpResponseRedirect('login')





def reg_tech(request):
    if request.method=='POST':
        frm_teachName = request.POST.get('teach_Name')
        frm_tech_Gender =request.POST.get('tech_Gender')
        frm_teach_Email = request.POST.get('teach_Email')
        frm_teach_Mobile = request.POST.get('teach_Mobile')
        frm_teach_UserName = request.POST.get('teach_UserName')
        frm_teach_PWD = request.POST.get('teach_PWD')

        print('Teacher Registration from Posted')
        saveTeacher = Teachers_Model(teach_Name=frm_teachName,tech_Gender=frm_tech_Gender,teach_Email=frm_teach_Email,teach_Mobile=frm_teach_Mobile,teach_UserName=frm_teach_UserName
        ,teach_PWD=frm_teach_PWD).save()

        request.session['UserName']=frm_teach_UserName
        return HttpResponseRedirect('dashboard')


    else:    
        return render(request,'teacher/reg.html',{})




def login(request):
    if request.method=='POST':
        login_type = request.POST.get('login_type')
        if(login_type=='teacher'):

            try:
                    userDeat = Teachers_Model.objects.get(teach_UserName=request.POST.get('login_UserName'),teach_PWD =request.POST.get('login_PWD') )
                    request.session['UserName']=userDeat.teach_UserName
                    return HttpResponseRedirect('teach_dashboard')

            except Teachers_Model.DoesNotExist:
                    context={
                    'err':"Check Credentials"
                }
            return render(request, 'login.html', context)
        if(login_type=='student'):

            try:
                    userDeat = Students_Model.objects.get(stdnt_UserName=request.POST.get('login_UserName'),stdnt_PWD =request.POST.get('login_PWD') )
                    request.session['stdnt_usr']=userDeat.stdnt_UserName
                    return HttpResponseRedirect('stdnt_dash')

            except Students_Model.DoesNotExist:
                    context={
                    'err':"Check Credentials"
                }
            return render(request, 'login.html', context)    

        

    else:

        return render(request, 'login.html')

def logout(request):

    request.session['UserName']=""
    request.session['stdnt_usr']=""

    return HttpResponseRedirect('login')


