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



def stdnt_dash(request):

    if 'stdnt_usr' in request.session:
            try:
                getDetails = Students_Model.objects.get(stdnt_UserName=request.session['stdnt_usr'])
                print (getDetails)
                context = {
                    'userName':getDetails.stdnt_UserName
                }
                return render(request, 'student/dashboard.html',context)
            except Students_Model.DoesNotExist:
                return HttpResponseRedirect('login')
    else:
            return HttpResponseRedirect('login')



def stdnt_nw_assignment(request):

    if 'stdnt_usr' in request.session:
                try:
                    getDetails = Students_Model.objects.get(stdnt_UserName=request.session['stdnt_usr'])
                    print (getDetails)
                    AssignmentListData = Assignments.objects.all()
                        
                    context = {
                                'userName':getDetails.stdnt_UserName,
                                'AssignmentListData':AssignmentListData,
                        }
                
                    return render(request, 'student/sbmnt_new_assignment.html',context)
                except Students_Model.DoesNotExist:
                    return HttpResponseRedirect('login')
    else:
            return HttpResponseRedirect('login')


def stdnt_upload_assignment(request):
    if 'stdnt_usr' in request.session:
            
                
                if request.method=="GET":
                    if request.GET.get('id'):
                        nameVar = request.session['stdnt_usr']
                        print(nameVar)
                        getDetails = Students_Model.objects.filter(stdnt_UserName=nameVar)[0]
                        AssignmentData = Assignments.objects.filter(assignment_id=request.GET.get('id'))
                        print(AssignmentData)

                        if len(AssignmentData)>0:
                            if request.GET.get('suc')=='updated':
                                context={
                                'userName':getDetails.stdnt_UserName,
                                'studentData':AssignmentData[0],
                                'suc':request.GET.get('suc')
                                }
                            else:
                                context = {
                                    'userName':getDetails.stdnt_UserName,
                                    'AssignmentData':AssignmentData[0],
                                    'StudentData':getDetails
                                }

                            return render(request, 'student/upload_assignment.html',context)
                        else:
                            return HttpResponseRedirect('stdnt_nw_assignment?id=invalid')
    
                    else:
                        return HttpResponseRedirect('stdnt_nw_assignment?id=invalid')


                if request.method=="POST":
                    frm_assignment_id = request.POST.get('assignment_id')
                    # print(frm_assignment_id)
                    frm_assignemt_stdnt_Roll = request.POST.get('assignmt_stdnt_Roll')
                    # print(frm_assignemt_stdnt_Roll)
                    frm_assignemt_file = request.FILES.get('uploadedFile')
                    frm_assignemt_submit_date = request.POST.get('upload_date_and_Time')
                    frm_assignment_status =request.POST.get('assignment_status')
                    frm_assignemt_review = request.POST.get('assignment_review')

                    assignmentDir = Assignments.objects.filter(assignment_id=frm_assignment_id)[0]
                    print(assignmentDir.assignment_DIR)
                    filePath = 'assignments/'+assignmentDir.assignment_DIR+'/'+frm_assignemt_stdnt_Roll+'_'+frm_assignemt_file.name

                   
                    print('Student Assignment Upload Posted')
                   
                    saveUploadAssignment = Assignemnt_Submissions(assignment_Model_ID=frm_assignment_id, assignment_submited_Roll= frm_assignemt_stdnt_Roll, assignment_submitted_File= filePath, assignment_submittion_date=frm_assignemt_submit_date, assignment_submittion_status=frm_assignment_status, assignment_submittion_review= frm_assignemt_review).save()
                    print(saveUploadAssignment)
                    handle_uploaded_file(filePath, frm_assignemt_file)

                    print('Student Assignment Update Succsesscull')
                    # id=request.POST.get('id')
                    passValue='stdnt_nw_assignment?suc=updated'
                    return HttpResponseRedirect(passValue)

           
    else:
            return HttpResponseRedirect('login')

def stdnt_view_assignments(request):
    
    if 'stdnt_usr' in request.session:
                try:
                    getDetails = Students_Model.objects.filter(stdnt_UserName=request.session['stdnt_usr'])
                    print (getDetails)
                    AssignmentListData = Assignemnt_Submissions.objects.filter(assignment_submited_Roll=getDetails[0].stdnt_Roll)
                        
                    context = {
                                'userName':getDetails[0].stdnt_UserName,
                                'AssignmentListData':AssignmentListData,
                                
                        }
                
                    return render(request, 'student/stdnt_view_assignments.html',context)
                except Students_Model.DoesNotExist:
                    return HttpResponseRedirect('login')
    else:
            return HttpResponseRedirect('login')



def stdnt_re_upload_assignment(request):
    if 'stdnt_usr' in request.session:
            
                
                if request.method=="GET":
                    if request.GET.get('id'):
                        nameVar = request.session['stdnt_usr']
                        print(nameVar)
                        getDetails = Students_Model.objects.filter(stdnt_UserName=nameVar)[0]
                        AssignmentData = Assignemnt_Submissions.objects.filter(assignment_submittion_id=request.GET.get('id'), assignment_submited_Roll=getDetails.stdnt_Roll)
                        assignmentModelData = Assignments.objects.filter(assignment_id=AssignmentData[0].assignment_Model_ID)
                        print(AssignmentData)

                        if len(AssignmentData)>0:
                            
                            context = {
                                'userName':getDetails.stdnt_UserName,
                                'AssignmentData':AssignmentData[0],
                                'StudentData':getDetails,
                                'AssignmentModel':assignmentModelData[0]
                            }

                            return render(request, 'student/re_upload_assignment.html',context)
                        else:
                            return HttpResponseRedirect('stdnt_nw_assignment?id=invalid')
    
                    else:
                        return HttpResponseRedirect('stdnt_nw_assignment?id=invalid')


                if request.method=="POST":
                    frm_assignment_id = request.POST.get('assignment_id')
                    # print(frm_assignment_id)
                    frm_assignemt_stdnt_Roll = request.POST.get('assignmt_stdnt_Roll')
                    # print(frm_assignemt_stdnt_Roll)
                    frm_assignemt_file = request.FILES.get('uploadedFile')
                    frm_assignemt_submit_date = request.POST.get('upload_date_and_Time')
                    frm_assignment_status =request.POST.get('assignment_status')
                    frm_assignemt_review = request.POST.get('assignment_review')

                    assignmentDir = Assignments.objects.filter(assignment_id=frm_assignment_id)[0]
                    print(assignmentDir.assignment_DIR)
                    filePath = 'assignments/'+assignmentDir.assignment_DIR+'/'+frm_assignemt_stdnt_Roll+'_'+frm_assignemt_file.name

                   
                    print('Student Assignment Upload Posted')
                   
                    saveUploadAssignment = Assignemnt_Submissions(assignment_Model_ID=frm_assignment_id, assignment_submited_Roll= frm_assignemt_stdnt_Roll, assignment_submitted_File= filePath, assignment_submittion_date=frm_assignemt_submit_date, assignment_submittion_status=frm_assignment_status, assignment_submittion_review= frm_assignemt_review).save()
                    print(saveUploadAssignment)
                    handle_uploaded_file(filePath, frm_assignemt_file)

                    print('Student Assignment Update Succsesscull')
                    # id=request.POST.get('id')
                    passValue='stdnt_nw_assignment?suc=updated'
                    return HttpResponseRedirect(passValue)

           
    else:
            return HttpResponseRedirect('login')        

def stdnt_del_assignment(request):
    if 'stdnt_usr' in request.session:
                try:
                    getDetails = Students_Model.objects.filter(stdnt_UserName=request.session['stdnt_usr'])
                    print (getDetails)
                    AssignmenttoDeleteVerify = Assignemnt_Submissions.objects.filter(assignment_submittion_id=request.GET.get('id'),assignment_submited_Roll=getDetails[0].stdnt_Roll)
                    print(AssignmenttoDeleteVerify.delete())

                    return HttpResponseRedirect('stdnt_view_assignments?del=suc')

                        
                   
                   
                except Students_Model.DoesNotExist:
                    return HttpResponseRedirect('login')
    else:
        return HttpResponseRedirect('login')



def handle_uploaded_file(file_passwd, file ):

# import docx2txt

# # Passing docx file to process function
# text = docx2txt.process("test.docx")

# # Saving content inside docx file into output.txt file
# with open("output.txt", "w") as text_file:
# 	print(text, file=text_file)


# import PyPDF2
 
# #create file object variable
# #opening method will be rb
# pdffileobj=open('1.pdf','rb')
 
# #create reader variable that will read the pdffileobj
# pdfreader=PyPDF2.PdfFileReader(pdffileobj)
 
# #This will store the number of pages of this pdf file
# x=pdfreader.numPages
 
# #create a variable that will select the selected number of pages
# pageobj=pdfreader.getPage(x+1)
 
# #(x+1) because python indentation starts with 0.
# #create text variable which will store all text datafrom pdf file
# text=pageobj.extractText()

    with open(file_passwd, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    print("file Uploaded")
