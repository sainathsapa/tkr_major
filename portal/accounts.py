import os
from django.conf import settings

from django.http.response import Http404
from portal.models import Assignments, Students_Model, Teachers_Model, Assignemnt_Submissions, Fees_Model, accounts_usr
from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.template import *
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, FormView
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext


def acc_dashboard(request):

    if 'Acc_UserName' in request.session:
        try:
            getDetails = accounts_usr.objects.get(
                acc_UserName=request.session['Acc_UserName'])
            print(getDetails)
            context = {
                'userName': getDetails.acc_Name
            }
            return render(request, 'accounts/dashboard.html', context)
        except accounts_usr.DoesNotExist:
            return HttpResponseRedirect('login')
    else:
        return HttpResponseRedirect('login')
        acc_view_stdnt


def acc_view_stdnt(request):
    if 'Acc_UserName' in request.session:
        try:
            getDetails = accounts_usr.objects.get(
                acc_UserName=request.session['Acc_UserName'])
            print(getDetails)
            studentData = Students_Model.objects.all()
            if request.GET.get('id'):
                context = {
                    'userName': getDetails.acc_Name,
                    'studentData': studentData,
                    'id': 'invalid'
                }
            else:
                context = {
                    'userName': getDetails.acc_Name,
                    'studentData': studentData,
                }

            return render(request, 'accounts/view_stdnts.html', context)
        except accounts_usr.DoesNotExist:
            return HttpResponseRedirect('login')
    else:
        return HttpResponseRedirect('login')


def acc_add_payment_type(request):
    if 'Acc_UserName' in request.session:
        try:
            getDetails = accounts_usr.objects.get(
                acc_UserName=request.session['Acc_UserName'])
            print(getDetails)
            print('Acc Logged')
            context = {
                'userName': getDetails.acc_UserName
            }
            if request.method == 'POST':
                frm_fees_paymentType = request.POST.get('payment_type')

                frm_fees_DESC = request.POST.get('fees_desc')

                frm_fees_amount = request.POST.get('fees_amount')

                print('Payments Addition Posted')

                saveNewPaymentMethod = Fees_Model(
                    fees_name=frm_fees_DESC, fees_type=frm_fees_paymentType, fees_amount=frm_fees_amount).save()
                print(saveNewPaymentMethod)
                print('Payment Details Saved Succsesscull')
                return HttpResponseRedirect('acc_add_payment_type?suc=added')

            return render(request, 'accounts/acc_add_payment_type.html', context)
        except accounts_usr.DoesNotExist:
            return HttpResponseRedirect('login')
    else:
        return HttpResponseRedirect('login')


def acc_view_payment_types(request):
    if 'Acc_UserName' in request.session:
        try:
            getDetails = accounts_usr.objects.get(
                acc_UserName=request.session['Acc_UserName'])
            print(getDetails)
            PaymentMethod = Fees_Model.objects.all()

            context = {
                'userName': getDetails.acc_UserName,
                'PaymentMethods': PaymentMethod,
            }

            return render(request, 'accounts/acc_view_payment_types.html', context)
        except Teachers_Model.DoesNotExist:
            return HttpResponseRedirect('login')
    else:
        return HttpResponseRedirect('login')


def acc_del_payment_method(request):

    if 'Acc_UserName' in request.session:

        try:
            DeletePaymentMethod = Fees_Model.objects.get(
                fees_id=request.GET.get('id'))

            # print(os.remove('assignments/'+DIR)

            print(DeletePaymentMethod.delete())

            print("acc_del_payment_method deleted successfully!")
            return HttpResponseRedirect('acc_view_payment_types?del=succ')

        except Exception as e:
            print(e)
            return HttpResponseRedirect('acc_view_payment_types?del=fail')

    else:
        return HttpResponseRedirect('login')
