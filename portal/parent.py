import os
from pickle import GET
from django.conf import settings
import urllib


from django.http.response import Http404
from flask import jsonify
from numpy import amax
from portal.models import Assignments, Books_Model, Parent_Model, Teachers_Model, Assignemnt_Submissions, Fees_Model, Payments_Model, Notices_Model, Book_Issue_Model, Attendance_model,Parent_Model
from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.template import *
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, FormView
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext


def parent_dash(request):

    if 'ParentUserName' in request.session:
        try:
            getDetails = Parent_Model.objects.get(
                parent_Mobile=request.session['ParentUserName'])
            print(getDetails)
            context = {
                'userName': getDetails.parent_Name
            }
            return render(request, 'parent/dashboard.html', context)
        except Parent_Model.DoesNotExist:
            return HttpResponseRedirect('login')
    else:
        return HttpResponseRedirect('login')


def stdnt_profile(request):
    if 'ParentUserName' in request.session:
        try:
            if request.method == 'GET':
                getDetails = Parent_Model.objects.get(
                    parent_Mobile=request.session['ParentUserName'])
                print(getDetails)
                studentData = Parent_Model.objects.filter(
                    parent_Mobile=request.session['ParentUserName'])
                print(studentData)

                if request.GET.get('suc') == 'updated':
                    context = {
                        'userName': getDetails.parent_Mobile,
                        'studentData': studentData[0],
                        'suc': request.GET.get('suc')
                    }
                else:
                    context = {
                        'userName': getDetails.parent_Mobile,
                        'studentData': studentData[0]
                    }

                return render(request, 'student/stdnt_profile.html', context)

            if request.method == "POST":
                frm_ParentUserNameName = request.POST.get('parent_Mobile')
                frm_stdnt_Roll = request.POST.get('stdnt_Roll')
                frm_stdnt_PWD = request.POST.get('stdnt_PWD')
                frm_stdnt_Email = request.POST.get('stdnt_Email')
                frm_stdnt_Gender = request.POST.get('stdnt_Gender')
                frm_stdnt_FLNM = request.POST.get('stdnt_NM')
                frm_stdnt_Branch = request.POST.get('stdnt_Branch')
                frm_stdnt_DOB = request.POST.get('stdnt_DOB')
                frm_stdnt_Mobile = request.POST.get('stdnt_mbl')
                frm_stdnt_active = request.POST.get('stdnt_status')
                print('Student Updated Posted')
                upDateStudent = Parent_Model.objects.filter(stdnt_id=request.POST.get('id')).update(stdnt_Name=frm_stdnt_FLNM, stdnt_Roll=frm_stdnt_Roll, stdnt_Branch=frm_stdnt_Branch, stdnt_DOB=frm_stdnt_DOB,
                                                                                                      stdnt_Gender=frm_stdnt_Gender, stdnt_Email=frm_stdnt_Email, stdnt_Mobile=frm_stdnt_Mobile, parent_Mobile=frm_ParentUserNameName, stdnt_PWD=frm_stdnt_PWD, stdnt_is_Active=frm_stdnt_active)
                print(upDateStudent)

                # saveStudent = Parent_Model(stdnt_Name=frm_stdnt_FLNM, stdnt_Roll=frm_stdnt_Roll, stdnt_Branch=frm_stdnt_Branch,stdnt_DOB=frm_stdnt_DOB,stdnt_Gender=frm_stdnt_Gender,stdnt_Email=frm_stdnt_Email,stdnt_Mobile=frm_stdnt_Mobile,parent_Mobile=frm_ParentUserNameName,stdnt_PWD=frm_stdnt_PWD,stdnt_is_Active=frm_stdnt_active).save()
                # print(saveStudent)

                return HttpResponseRedirect('stdnt_dash')

        except Parent_Model.DoesNotExist:
            return HttpResponseRedirect('login')
    else:
        return HttpResponseRedirect('login')


def parent_stdnt_view_assignments(request):

    if 'ParentUserName' in request.session:
        try:
            getDetails = Parent_Model.objects.get(
                parent_Mobile=request.session['ParentUserName'])
            print(getDetails)
            AssignmentListData = Assignemnt_Submissions.objects.filter(
                assignment_submited_Roll=getDetails.parent_stdnt_Roll.stdnt_Roll)

            context = {
                'userName': getDetails.parent_Name,
                'AssignmentListData': AssignmentListData,

            }

            return render(request, 'parent/parent_stdnt_view_assignments.html', context)
        except Parent_Model.DoesNotExist:
            return HttpResponseRedirect('login')
    else:
        return HttpResponseRedirect('login')


def stdnt_re_upload_assignment(request):
    if 'ParentUserName' in request.session:

        if request.method == "GET":
            if request.GET.get('id'):
                nameVar = request.session['ParentUserName']
                print(nameVar)
                getDetails = Parent_Model.objects.filter(
                    parent_Mobile=nameVar)[0]
                AssignmentData = Assignemnt_Submissions.objects.filter(
                    assignment_submittion_id=request.GET.get('id'), assignment_submited_Roll=getDetails.stdnt_Roll)
                assignmentModelData = Assignments.objects.filter(
                    assignment_id=AssignmentData[0].assignment_Model_ID)
                print(AssignmentData)

                if len(AssignmentData) > 0:

                    context = {
                        'userName': getDetails.parent_Mobile,
                        'AssignmentData': AssignmentData[0],
                        'StudentData': getDetails,
                        'AssignmentModel': assignmentModelData[0]
                    }

                    return render(request, 'student/re_upload_assignment.html', context)
                else:
                    return HttpResponseRedirect('stdnt_nw_assignment?id=invalid')

            else:
                return HttpResponseRedirect('stdnt_nw_assignment?id=invalid')

        if request.method == "POST":
            frm_assignment_id = request.POST.get('assignment_id')
            # print(frm_assignment_id)
            frm_assignemt_stdnt_Roll = request.POST.get('assignmt_stdnt_Roll')
            # print(frm_assignemt_stdnt_Roll)
            frm_assignemt_file = request.FILES.get('uploadedFile')
            frm_assignemt_submit_date = request.POST.get(
                'upload_date_and_Time')
            frm_assignment_status = request.POST.get('assignment_status')
            frm_assignemt_review = request.POST.get('assignment_review')

            assignmentDir = Assignments.objects.filter(
                assignment_id=frm_assignment_id)[0]
            print(assignmentDir.assignment_DIR)
            filePath = 'assignments/'+assignmentDir.assignment_DIR + \
                '/'+frm_assignemt_stdnt_Roll+'_'+frm_assignemt_file.name

            print('Student Assignment Upload Posted')

            saveUploadAssignment = Assignemnt_Submissions(assignment_Model_ID=frm_assignment_id, assignment_submited_Roll=frm_assignemt_stdnt_Roll, assignment_submitted_File=filePath,
                                                          assignment_submittion_date=frm_assignemt_submit_date, assignment_submittion_status=frm_assignment_status, assignment_submittion_review=frm_assignemt_review).save()
            print(saveUploadAssignment)
            handle_uploaded_file(filePath, frm_assignemt_file)

            print('Student Assignment Update Succsesscull')
            # id=request.POST.get('id')
            passValue = 'stdnt_nw_assignment?suc=updated'
            return HttpResponseRedirect(passValue)

    else:
        return HttpResponseRedirect('login')


def stdnt_del_assignment(request):
    if 'ParentUserName' in request.session:
        try:
            getDetails = Parent_Model.objects.filter(
                parent_Mobile=request.session['ParentUserName'])
            print(getDetails)
            AssignmenttoDeleteVerify = Assignemnt_Submissions.objects.filter(
                assignment_submittion_id=request.GET.get('id'), assignment_submited_Roll=getDetails[0].stdnt_Roll)
            print(AssignmenttoDeleteVerify.delete())

            return HttpResponseRedirect('stdnt_view_assignments?del=suc')

        except Parent_Model.DoesNotExist:
            return HttpResponseRedirect('login')
    else:
        return HttpResponseRedirect('login')


def stdnt_nw_payment(request):
    if 'ParentUserName' in request.session:

        if request.method == "GET":
            nameVar = request.session['ParentUserName']
            print(nameVar)
            getDetails = Parent_Model.objects.filter(
                parent_Mobile=nameVar)[0]
            Fees_Model_data = Fees_Model.objects.all()
            print(Fees_Model_data)

            if len(Fees_Model_data) > 0:
                if request.GET.get('suc') == 'updated':
                    context = {
                        'userName': getDetails.parent_Mobile,
                        'studentData': Fees_Model_data[0],
                        'suc': request.GET.get('suc')
                    }
                else:
                    context = {
                        'userName': getDetails.parent_Mobile,
                        'FeesDetails': Fees_Model_data,
                        'StudentData': getDetails
                    }

                return render(request, 'student/stdnt_mk_payment.html', context)
            else:
                return "{NOt Valid}"

    else:
        return HttpResponseRedirect('login')


def stdnt_indvid_mk_payment(request):
    if 'ParentUserName' in request.session:

        if request.method == "GET":
            if request.GET.get('id'):
                nameVar = request.session['ParentUserName']
                print(nameVar)
                getDetails = Parent_Model.objects.filter(
                    parent_Mobile=nameVar)[0]
                PaymentData = Fees_Model.objects.filter(
                    fees_id=request.GET.get('id'))
                print(PaymentData)

                if len(PaymentData) > 0:
                    if request.GET.get('suc') == 'updated':
                        context = {
                            'userName': getDetails.parent_Mobile,
                            'PaymentData': PaymentData[0],
                            'suc': request.GET.get('suc')
                        }
                    else:
                        context = {
                            'userName': getDetails.parent_Mobile,
                            'PaymentData': PaymentData[0],
                            'StudentData': getDetails
                        }

                    return render(request, 'student/stdnt_indvid_mk_payment.html', context)
                else:
                    return HttpResponseRedirect('stdnt_nw_payment?id=invalid')

            else:
                return HttpResponseRedirect('stdnt_nw_payment?id=invalid')

        if request.method == "POST":

            frm_fees_type = request.POST.get('frm_fees_type')
            frm_fees_submited_Roll = request.POST.get('frm_fees_submited_Roll')
            frm_fee_razorpay_id = request.POST.get('razorpay_payment_id')
            frm_payment_state = request.POST.get('frm_payment_state')
            frm_fees_amount = request.POST.get('frm_fees_amount')
            reason = request.POST.get('reason')

            print(frm_payment_state)
            if reason == "Success":
                SavePayment = Payments_Model(fees_type=frm_fees_type, fees_submited_Roll=frm_fees_submited_Roll, razorpay_payment_id=frm_fee_razorpay_id,
                                             payment_state=frm_payment_state, reason="Success", amount=frm_fees_amount).save()
                passValue = 'stdnt_nw_payment?suca=success'
                return HttpResponseRedirect(passValue)
            else:
                SavePayment = Payments_Model(fees_type=frm_fees_type, fees_submited_Roll=frm_fees_submited_Roll, razorpay_payment_id=frm_fee_razorpay_id,
                                             payment_state=frm_payment_state, reason=reason, amount=frm_fees_amount).save()
                passValue = 'stdnt_nw_payment?sucl=failed'
                return HttpResponseRedirect(passValue)

            # id=request.POST.get('id')

    else:
        return HttpResponseRedirect('login')


def stdnt_view_payments(request):

    if 'ParentUserName' in request.session:
        try:
            getDetails = Parent_Model.objects.filter(
                parent_Mobile=request.session['ParentUserName'])
            print(getDetails)
            PaymentsData = Payments_Model.objects.filter(
                fees_submited_Roll=getDetails[0].stdnt_Roll)

            context = {
                'userName': getDetails[0].parent_Mobile,
                'PaymentsData': PaymentsData,

            }

            return render(request, 'student/stdnt_view_payments.html', context)
        except Parent_Model.DoesNotExist:
            return HttpResponseRedirect('login')
    else:
        return HttpResponseRedirect('login')


def parent_view_notices(request):
    if 'ParentUserName' in request.session:
        try:
            getDetails = Parent_Model.objects.get(
                parent_Mobile=request.session['ParentUserName'])
            print(getDetails)
            NoticesData = Notices_Model.objects.all()

            context = {
                'userName': getDetails.parent_Name,
                'NoticesData': NoticesData,
            }

            return render(request, 'parent/parent_stdnt_view_notices.html', context)
        except Parent_Model.DoesNotExist:
            return HttpResponseRedirect('login')
    else:
        return HttpResponseRedirect('login')


def parent_view_notice(request):
    if 'ParentUserName' in request.session:
        try:
            getDetails = Parent_Model.objects.get(
                parent_Mobile=request.session['ParentUserName'])
            print(getDetails)
            NoticesData = Notices_Model.objects.filter(
                notice_id=request.GET.get('notice_id'))

            context = {
                'userName': getDetails.parent_Name,
                'NoticesData': NoticesData[0],
            }

            return render(request, 'parent/parent_stdnt_view_notice.html', context)
        except Parent_Model.DoesNotExist:
            return HttpResponseRedirect('login')
    else:
        return HttpResponseRedirect('login')


def stdnt_view_book(request):
    if 'ParentUserName' in request.session:
        try:
            getDetails = Parent_Model.objects.get(
                parent_Mobile=request.session['ParentUserName'])
            print(getDetails)
            BookData = Books_Model.objects.filter(
                book_id=request.GET.get('id'))

            context = {
                'userName': getDetails.stdnt_Name,
                'BookData': BookData[0],
            }

            return render(request, 'student/stdnt_view_book.html', context)
        except Parent_Model.DoesNotExist:
            return HttpResponseRedirect('login')
    else:
        return HttpResponseRedirect('login')


def parent_stdnt_lib_pending_books(request):
    if 'ParentUserName' in request.session:
        try:
            getDetails = Parent_Model.objects.get(
                parent_Mobile=request.session['ParentUserName'])
            print(getDetails)
            PendingBookReq = Book_Issue_Model.objects.filter(
                book_borrower_roll=getDetails.parent_stdnt_Roll.stdnt_Roll, book_issue_state="Pending")

            context = {
                'userName': getDetails.parent_Name,
                'roll_number': getDetails.parent_stdnt_Roll.stdnt_Roll,
                'PendingBookReq': PendingBookReq,

            }

            return render(request, 'parent/parent_stdnt_view_pending_req.html', context)
        except Parent_Model.DoesNotExist:
            return HttpResponseRedirect('login')
    else:
        return HttpResponseRedirect('login')



def parent_stdnt_results(request):
    if 'ParentUserName' in request.session:
        try:
            getDetails = Parent_Model.objects.get(
                parent_Mobile=request.session['ParentUserName'])
            print(getDetails)
            PendingBookReq = Book_Issue_Model.objects.filter(
                book_borrower_roll=getDetails.stdnt_Roll, book_issue_state="Pending")

            context = {
                'userName': getDetails.stdnt_Name,
                'roll_number': getDetails.stdnt_Roll,
                'PendingBookReq': PendingBookReq,

            }

            return render(request, 'student/stdnt_results.html', context)
        except Parent_Model.DoesNotExist:
            return HttpResponseRedirect('login')
    else:
        return HttpResponseRedirect('login')


def parent_stdnt_attendance(request):
    if 'ParentUserName' in request.session:
        try:
            getDetails = Parent_Model.objects.get(
                parent_Mobile=request.session['ParentUserName'])
            print(getDetails)
            AttendanceModel = Attendance_model.objects.all()
            context = {
                'userName': getDetails.parent_Name,
                'roll_number': getDetails.parent_stdnt_Roll,
            }
            listTemp = {}
            for i in AttendanceModel:
                listTemp[str(i.attendance_date)] = {'date': i.attendance_date,'present': i.attendance_json_field.get(
                    getDetails.parent_stdnt_Roll), 'addedBY': i.attendance_added_by, 'addedAt': i.attendance_added_at}
            context['listTemp'] = listTemp

            return render(request, 'parent/parent_stdnt_view_attendance.html', context)
        except Parent_Model.DoesNotExist:
            return HttpResponseRedirect('login')
    else:
        return HttpResponseRedirect('login')

