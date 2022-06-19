import os
import random
import re
from django.conf import settings

from django.http.response import Http404
from regex import P
from portal.models import Students_Model, Library_User_Model, Books_Model, Notices_Model
from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.template import *
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, FormView
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext


def lib_dashboard(request):

    if 'LibUserName' in request.session:
        try:
            getDetails = Library_User_Model.objects.get(
                lib_userName=request.session['LibUserName'])
            print(getDetails)
            context = {
                'userName': getDetails.lib_userName
            }
            return render(request, 'library/dashboard.html', context)
        except Library_User_Model.DoesNotExist:
            return HttpResponseRedirect('login')
    else:
        return HttpResponseRedirect('login')
        acc_view_stdnt


def lib_view_stdnts(request):
    if 'LibUserName' in request.session:
        try:
            getDetails = Library_User_Model.objects.get(
                lib_userName=request.session['LibUserName'])
            print(getDetails)
            studentData = Students_Model.objects.all()
            if request.GET.get('id'):
                context = {
                    'userName': getDetails.lib_userName,
                    'studentData': studentData,
                    'id': 'invalid'
                }
            else:
                context = {
                    'userName': getDetails.lib_userName,
                    'studentData': studentData,
                }

            return render(request, 'library/view_stdnts.html', context)
        except Library_User_Model.DoesNotExist:
            return HttpResponseRedirect('login')
    else:
        return HttpResponseRedirect('login')


def lib_add_new_book(request):
    if 'LibUserName' in request.session:
        try:
            getDetails = Library_User_Model.objects.get(
                lib_userName=request.session['LibUserName'])
            print(getDetails)
            print('Acc Logged')
            context = {
                'userName': getDetails.lib_userName
            }
            if request.method == 'POST':
                POST = request.POST
                frm_branch = POST.get('branch_name')
                frm_book_nm = POST.get('book_name')
                frm_book_description = POST.get('book_desc')
                frm_book_author = POST.get('book_author')
                frm_book_stock = POST.get('book_stock')
                frm_book_image = request.FILES.get('book_img')
                Random_filename = str(random.random())+frm_book_image.name
                filePath = 'assignments/book_img/lib/'+Random_filename
                print('Book Addition Posted')
                handle_uploaded_file(filePath, frm_book_image)
                saveBook = Books_Model(book_Name=frm_book_nm, book_author=frm_book_author, book_img=filePath,
                                       book_special_category=frm_branch, book_desc=frm_book_description, book_stock=frm_book_stock, book_addedBy=getDetails.lib_userName).save()
                print(saveBook)
                print('Book Details Saved Succsesscull')
                return HttpResponseRedirect('lib_add_new_book?suc=added')

            return render(request, 'library/lib_add_new_book.html', context)
        except Library_User_Model.DoesNotExist:
            return HttpResponseRedirect('login')
    else:
        return HttpResponseRedirect('login')


def lib_view_books(request):
    if 'LibUserName' in request.session:
        try:
            getDetails = Library_User_Model.objects.get(
                lib_userName=request.session['LibUserName'])
            print(getDetails)
            BooksData = Books_Model.objects.all()

            context = {
                'userName': getDetails.lib_userName,
                'BooksData': BooksData,
            }

            return render(request, 'library/lib_view_books.html', context)
        except Library_User_Model.DoesNotExist:
            return HttpResponseRedirect('login')
    else:
        return HttpResponseRedirect('login')


def lib_edit_book(request):
    if 'LibUserName' in request.session:

        if request.method == "GET":
            if request.GET.get('id'):

                getDetails = Library_User_Model.objects.get(
                    lib_userName=request.session['LibUserName'])
                print(getDetails)
                BookData = Books_Model.objects.filter(
                    book_id=request.GET.get('id'))
                if (BookData.count() < 0):
                    return HttpResponseRedirect('lib_view_books?id=invalid')

                context = {
                    'userName': getDetails.lib_userName,
                    'BookData': BookData[0]
                }

                return render(request, 'library/lib_edit_book.html', context)

            else:
                return HttpResponseRedirect('lib_view_books?id=invalid')

        if request.method == 'POST':
            POST = request.POST
            frm_book_id = POST.get('book_id')
            frm_branch = POST.get('book_branch')
            frm_book_nm = POST.get('book_name')
            frm_book_description = POST.get('book_desc')
            frm_book_author = POST.get('book_author')
            frm_book_stock = POST.get('book_stock')
            print('Book Addition Posted')
            UploadBook = Books_Model.objects.filter(book_id=frm_book_id).update(book_Name=frm_book_nm, book_author=frm_book_author,
                                                                                book_special_category=frm_branch, book_desc=frm_book_description, book_stock=frm_book_stock)
            print(UploadBook)
            print('Book Details Updated')
            return HttpResponseRedirect('lib_view_books?suc=updated')
    else:
        return HttpResponseRedirect('login')


def lib_del_book(request):

    if 'LibUserName' in request.session:

        try:
            DeleteBook = Books_Model.objects.get(
                book_id=request.GET.get('id'))

            # print(os.remove('assignments/'+DIR)

            print(DeleteBook.delete())

            print("Book deleted successfully!")
            return HttpResponseRedirect('lib_view_books?del=succ')

        except Exception as e:
            print(e)
            return HttpResponseRedirect('lib_view_books?del=fail')

    else:
        return HttpResponseRedirect('login')


def acc_view_payments(request):

    if 'LibUserName' in request.session:

        getDetails = Library_User_Model.objects.get(
            LibUserName=request.session['LibUserName'])
        print(getDetails)
        Payments = Payments_Model.objects.all()

        context = {
            'userName': getDetails.lib_userName,
            'PaymentsData': Payments

        }

        return render(request, 'accounts/acc_view_payments.html', context)
    else:
        return HttpResponseRedirect('login')


def acc_sdnt_view_payments(request):
    if 'LibUserName' in request.session:
        try:
            if request.GET.get('stdnt_Roll'):

                getDetails = Library_User_Model.objects.get(
                    LibUserName=request.session['LibUserName'])
                print(getDetails)
                PaymentsData = Payments_Model.objects.filter(
                    fees_submited_Roll=request.GET.get('stdnt_Roll'))

                context = {
                    'userName': getDetails.lib_userName,
                    'PaymentsData': PaymentsData,

                }

                return render(request, 'accounts/acc_stdnt_view_payments.html', context)
        except Students_Model.DoesNotExist:
            return HttpResponseRedirect('login')
    else:
        return HttpResponseRedirect('login')


def acc_add_notices(request):
    if 'LibUserName' in request.session:
        try:
            getDetails = Library_User_Model.objects.get(
                LibUserName=request.session['LibUserName'])
            print(getDetails)
            print('Acc Logged')
            context = {
                'userName': getDetails.LibUserName
            }

            if request.method == 'POST':
                POST = request.POST
                notice_added_user = getDetails.LibUserName
                notice_name = POST.get('notice_name')
                notice_description = POST.get('notice_description')

                SaveNotice = Notices_Model(
                    notice_added_user=notice_added_user, notice_name=notice_name, notice_description=notice_description).save()
                print(SaveNotice)
                return HttpResponseRedirect('acc_add_notice?suc=added')

            return render(request, 'accounts/acc_add_notice.html', context)
        except Library_User_Model.DoesNotExist:
            return HttpResponseRedirect('login')
    else:
        return HttpResponseRedirect('login')


def acc_view_notices(request):
    if 'LibUserName' in request.session:
        try:
            getDetails = Library_User_Model.objects.get(
                LibUserName=request.session['LibUserName'])
            print(getDetails)
            NoticesData = Notices_Model.objects.all()

            context = {
                'userName': getDetails.LibUserName,
                'NoticesData': NoticesData,
            }

            return render(request, 'accounts/acc_view_notices.html', context)
        except Library_User_Model.DoesNotExist:
            return HttpResponseRedirect('login')
    else:
        return HttpResponseRedirect('login')


def acc_view_notice(request):
    if 'LibUserName' in request.session:
        try:
            getDetails = Library_User_Model.objects.get(
                LibUserName=request.session['LibUserName'])
            print(getDetails)
            NoticesData = Notices_Model.objects.filter(
                notice_id=request.GET.get('notice_id'))

            context = {
                'userName': getDetails.LibUserName,
                'NoticesData': NoticesData[0],
            }

            return render(request, 'accounts/acc_view_notice.html', context)
        except Library_User_Model.DoesNotExist:
            return HttpResponseRedirect('login')
    else:
        return HttpResponseRedirect('login')


def handle_uploaded_file(file_passwd, file):

    with open(file_passwd, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    print("file Uploaded")
