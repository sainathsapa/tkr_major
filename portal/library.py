from asyncio.windows_events import NULL
import os
import random
import re
from django.conf import settings
from datetime import datetime, timedelta

from django.db.models import F

from django.http.response import Http404
from regex import P
from portal.models import Book_Issue_Model, Students_Model, Library_User_Model, Books_Model, Notices_Model
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


def lib_view_borrow_req(request):

    if 'LibUserName' in request.session:

        getDetails = Library_User_Model.objects.get(
            lib_userName=request.session['LibUserName'])
        print(getDetails)
        PendingBookReq = Book_Issue_Model.objects.filter(
            book_issue_state="Pending")

        context = {
            'userName': getDetails.lib_userName,
            'PendingBookReq': PendingBookReq

        }

        return render(request, 'library/lib_view_borrow_req.html', context)
    else:
        return HttpResponseRedirect('login')


def lib_view_specific_book_req(request):
    if 'LibUserName' in request.session:

        getDetails = Library_User_Model.objects.get(
            lib_userName=request.session['LibUserName'])
        print(getDetails)
        book_id = request.GET.get('id')
        BookSpecData = Book_Issue_Model.objects.filter(
            book_borrow_book_id=book_id)

        context = {
            'userName': getDetails.lib_userName,
            'BookSpecData': BookSpecData

        }
        print(book_id)
        return render(request, 'library/lib_view_spec_book_req.html', context)
    else:
        return HttpResponseRedirect('login')


def lib_del_borrow_req(request):
    if 'LibUserName' in request.session:

        try:
            DeleteBookIssue = Book_Issue_Model.objects.get(
                book_issue_id=request.GET.get('book_issue_id'))

            # print(os.remove('assignments/'+DIR)

            print(DeleteBookIssue.delete())

            print("Book Req deleted successfully!")
            return HttpResponseRedirect('lib_view_borrow_req?del=suc')

        except Exception as e:
            print(e)
            return HttpResponseRedirect('stdnt_lib_pending_books?del=fail')

    else:
        return HttpResponseRedirect('login')


def lib_update_book_rq(request):
    if 'LibUserName' in request.session:
        if request.method == 'GET':
            getDetails = Library_User_Model.objects.get(
                lib_userName=request.session['LibUserName'])
            print(getDetails)
            book_RQ_id = request.GET.get('id')
            BookRQDATA = Book_Issue_Model.objects.filter(
                book_issue_id=book_RQ_id)

            context = {
                'userName': getDetails.lib_userName,
                'BookRQDATA': BookRQDATA[0]

            }
            print(BookRQDATA)
            return render(request, 'library/lib_update_book_rq.html', context)
        if request.method == 'POST':
            frm_POST_book_issueID = request.POST.get('id')
            frm_book_id = request.POST.get('book_id')[-1]
            dt_string = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")

            UpdateBookIssue = Book_Issue_Model.objects.filter(book_issue_id=frm_POST_book_issueID).update(
                book_issue_state="Issued", book_issue_date=dt_string)
            if(UpdateBookIssue):
                Books_Model.objects.filter(book_id=frm_book_id).update(
                    book_stock=F('book_stock')-1)

            return HttpResponseRedirect('lib_view_borrow_req?update=suc')
    else:
        return HttpResponseRedirect('login')


def lib_book_issues(request):
    if 'LibUserName' in request.session:
        try:
            getDetails = Library_User_Model.objects.get(
                lib_userName=request.session['LibUserName'])
            print(getDetails)
            BookIssueData = Book_Issue_Model.objects.filter(
                book_issue_state="Issued")

            context = {
                'userName': getDetails.lib_userName,
                'PendingBookReq': BookIssueData,

            }

            return render(request, 'library/lib_view_borrow_req.html', context)
        except Students_Model.DoesNotExist:
            return HttpResponseRedirect('login')
    else:
        return HttpResponseRedirect('login')


def lib_pending_books(request):
    if 'LibUserName' in request.session:
        try:
            getDetails = Library_User_Model.objects.get(
                lib_userName=request.session['LibUserName'])
            print(getDetails)


            futuredate = datetime.now() + timedelta(days=-1)
            futuredate=futuredate.strftime("%Y-%m-%d-%H:%M:%S")
            BookIssueData=Book_Issue_Model.objects.all()

            context={
                'userName': getDetails.lib_userName,
                'BookIssueData': BookIssueData,
                'dt':futuredate


            }

            return render(request, 'library/lib_view_borrow_pending.html', context)
        except Students_Model.DoesNotExist:
            return HttpResponseRedirect('login')
    else:
        return HttpResponseRedirect('login')


def lib_add_notices(request):
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
                notice_added_user = getDetails.lib_userName
                notice_name = POST.get('notice_name')
                notice_description = POST.get('notice_description')

                SaveNotice = Notices_Model(
                    notice_added_user=notice_added_user, notice_name=notice_name, notice_description=notice_description).save()
                print(SaveNotice)
                return HttpResponseRedirect('lib_add_notice?suc=added')

            return render(request, 'library/lib_add_notice.html', context)
        except Library_User_Model.DoesNotExist:
            return HttpResponseRedirect('login')
    else:
        return HttpResponseRedirect('login')


def lib_view_notices(request):
    if 'LibUserName' in request.session:
        try:
            getDetails = Library_User_Model.objects.get(
                lib_userName=request.session['LibUserName'])
            print(getDetails)
            NoticesData = Notices_Model.objects.all()

            context = {
                'userName': getDetails.lib_userName,
                'NoticesData': NoticesData,
            }

            return render(request, 'library/lib_view_notices.html', context)
        except Library_User_Model.DoesNotExist:
            return HttpResponseRedirect('login')
    else:
        return HttpResponseRedirect('login')


def lib_view_notice(request):
    if 'LibUserName' in request.session:
        try:
            getDetails = Library_User_Model.objects.get(
                lib_userName=request.session['LibUserName'])
            print(getDetails)
            NoticesData = Notices_Model.objects.filter(
                notice_id=request.GET.get('notice_id'))

            context = {
                'userName': getDetails.lib_userName,
                'NoticesData': NoticesData[0],
            }

            return render(request, 'library/lib_view_notice.html', context)
        except Library_User_Model.DoesNotExist:
            return HttpResponseRedirect('login')
    else:
        return HttpResponseRedirect('login')


def handle_uploaded_file(file_passwd, file):

    with open(file_passwd, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    print("file Uploaded")
