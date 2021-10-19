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


def teach_dash(request):

    if 'UserName' in request.session:
        try:
            getDetails = Teachers_Model.objects.get(teach_UserName=request.session['UserName'])
            print (getDetails)
            context = {
                'userName':getDetails.teach_UserName
            }
            return render(request, 'teacher/dashboard.html',context)
        except Teachers_Model.DoesNotExist:
            return HttpResponseRedirect('login')
    else:
            return HttpResponseRedirect('login')





def teach_add_sdnt(request):

    if 'UserName' in request.session:
            try:
                getDetails = Teachers_Model.objects.get(teach_UserName=request.session['UserName'])
                print (getDetails)
                print('Teacher Logged')
                context = {
                    'userName':getDetails.teach_UserName
                }
                if request.method=='POST':
                    frm_stdnt_USRName = request.POST.get('stdnt_username')
                    frm_stdnt_Roll = request.POST.get('stdnt_Roll')
                    frm_stdnt_PWD = request.POST.get('stdnt_PWD')
                    frm_stdnt_Email = request.POST.get('stdnt_Email')
                    frm_stdnt_Gender = request.POST.get('stdnt_Gender')
                    frm_stdnt_FLNM = request.POST.get('stdnt_NM')
                    frm_stdnt_Branch = request.POST.get('stdnt_Branch')
                    frm_stdnt_DOB = request.POST.get('stdnt_DOB')
                    frm_stdnt_Mobile = request.POST.get('stdnt_mbl')
                    frm_stdnt_active = request.POST.get('stdnt_status')
                    print('Student Addition Posted')
                    saveStudent = Students_Model(stdnt_Name=frm_stdnt_FLNM, stdnt_Roll=frm_stdnt_Roll, stdnt_Branch=frm_stdnt_Branch,stdnt_DOB=frm_stdnt_DOB,stdnt_Gender=frm_stdnt_Gender,stdnt_Email=frm_stdnt_Email,stdnt_Mobile=frm_stdnt_Mobile,stdnt_UserName=frm_stdnt_USRName,stdnt_PWD=frm_stdnt_PWD,stdnt_is_Active=frm_stdnt_active).save()
                    print(saveStudent)
                    print('Student Details Saved Succsesscull')
                    return HttpResponseRedirect('teach_add_stdnt?suc=added')



                else:    
                    if request.GET.get('suc')=='added':
                        context={
                        'userName':getDetails.teach_UserName,
                        'msg':'Student Added Sucessfully'

                        }
                        return render(request, 'teacher/add_stdnt.html',context)

                    return render(request, 'teacher/add_stdnt.html',context)
            except Teachers_Model.DoesNotExist:
                return HttpResponseRedirect('login')
    else:
            return HttpResponseRedirect('login')


def teach_view_stdnt(request):
    if 'UserName' in request.session:
            try:
                getDetails = Teachers_Model.objects.get(teach_UserName=request.session['UserName'])
                print (getDetails)
                studentData = Students_Model.objects.all()
                if request.GET.get('id'):
                    context = {
                        'userName':getDetails.teach_UserName,
                        'studentData':studentData,
                        'id':'invalid'
                    }
                else:
                       context = {
                        'userName':getDetails.teach_UserName,
                        'studentData':studentData,
                    }

                return render(request, 'teacher/view_stdnts.html',context)
            except Teachers_Model.DoesNotExist:
                return HttpResponseRedirect('login')
    else:
            return HttpResponseRedirect('login')



def teach_edit_stdnt(request):
    if 'UserName' in request.session:
            try:
                
                if request.method=="GET":
                    if request.GET.get('id'):
                        getDetails = Teachers_Model.objects.get(teach_UserName=request.session['UserName'])
                        print (getDetails)
                        studentData = Students_Model.objects.filter(stdnt_id=request.GET.get('id'))
                        print(studentData)

                        if request.GET.get('suc')=='updated':
                            context={
                            'userName':getDetails.teach_UserName,
                            'studentData':studentData[0],
                            'suc':request.GET.get('suc')
                            }
                        else:
                            context = {
                                'userName':getDetails.teach_UserName,
                                'studentData':studentData[0]
                            }

                        return render(request, 'teacher/edit_stdnt.html',context)
                    else:
                        return HttpResponseRedirect('teach_view_stdnt?id=invalid')


                if request.method=="POST":
                    frm_stdnt_USRName = request.POST.get('stdnt_username')
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
                    upDateStudent = Students_Model.objects.filter(stdnt_id=request.POST.get('id')).update(stdnt_Name=frm_stdnt_FLNM, stdnt_Roll=frm_stdnt_Roll, stdnt_Branch=frm_stdnt_Branch,stdnt_DOB=frm_stdnt_DOB,stdnt_Gender=frm_stdnt_Gender,stdnt_Email=frm_stdnt_Email,stdnt_Mobile=frm_stdnt_Mobile,stdnt_UserName=frm_stdnt_USRName,stdnt_PWD=frm_stdnt_PWD,stdnt_is_Active=frm_stdnt_active)
                    print(upDateStudent)


                    # saveStudent = Students_Model(stdnt_Name=frm_stdnt_FLNM, stdnt_Roll=frm_stdnt_Roll, stdnt_Branch=frm_stdnt_Branch,stdnt_DOB=frm_stdnt_DOB,stdnt_Gender=frm_stdnt_Gender,stdnt_Email=frm_stdnt_Email,stdnt_Mobile=frm_stdnt_Mobile,stdnt_UserName=frm_stdnt_USRName,stdnt_PWD=frm_stdnt_PWD,stdnt_is_Active=frm_stdnt_active).save()
                    # print(saveStudent)
                    print('Student Details Update Succsesscull')
                    id=request.POST.get('id')
                    passValue='teach_edit_stdnt?suc=updated'+'&id='+id
                    return HttpResponseRedirect(passValue)

            except Teachers_Model.DoesNotExist:
                return HttpResponseRedirect('login')
    else:
            return HttpResponseRedirect('login')


def teach_del_stdnt(request):
    if 'UserName' in request.session:
        try:
            try:
                DelStudentData = Students_Model.objects.get(stdnt_id=request.GET.get('id'))
                print(DelStudentData.delete())

                
                print("Student deleted successfully!")
                return HttpResponseRedirect('teach_view_stdnt?del=succ')

            except:
                print("Student doesn't exists")
                return HttpResponseRedirect('teach_view_stdnt?del=fail')

        except Teachers_Model.DoesNotExist:
            return HttpResponseRedirect('login')
    else:
            return HttpResponseRedirect('login')        
    


def teach_nw_assign(request):
    if 'UserName' in request.session:
            try:
                getDetails = Teachers_Model.objects.get(teach_UserName=request.session['UserName'])
                print (getDetails)
                print('Teacher Logged')
                context = {
                    'userName':getDetails.teach_UserName
                }
                if request.method=='POST':
                    frm_assign_DIRNAME = request.POST.get('assgin_DirName')
                    frm_assign_Marks = request.POST.get('assgin_Marks')
                    frm_assign_FileType = request.POST.get('file_type')

                    frm_assign_LastDate = request.POST.get('assign_LastDate')
                    frm_assign_QN = request.POST.get('assign_QN')
                   
                    print('Assignment Addition Posted')
                                    
                    if not os.path.exists('assignments/'+frm_assign_DIRNAME):
                        os.makedirs('assignments/'+frm_assign_DIRNAME)

                    saveNewAssignment = Assignments(assignment_DIR=frm_assign_DIRNAME, assignment_QN=frm_assign_QN, assignment_Marks=frm_assign_Marks,assignment_Last_Date=frm_assign_LastDate,assignment_FileType=frm_assign_FileType, assignment_status=True).save()
                    print(saveNewAssignment)
                    print('Assignememnt Details Saved Succsesscull')
                    return HttpResponseRedirect('teach_nw_assignment?suc=added')
               

                return render(request, 'teacher/nw_assignment.html',context)
            except Teachers_Model.DoesNotExist:
                return HttpResponseRedirect('login')
    else:
            return HttpResponseRedirect('login')



def teach_lst_assign(request):

        if 'UserName' in request.session:
                    try:
                        getDetails = Teachers_Model.objects.get(teach_UserName=request.session['UserName'])
                        print (getDetails)
                        AssignmentListData = Assignments.objects.all()
                        
                        context = {
                                'userName':getDetails.teach_UserName,
                                'AssignmentListData':AssignmentListData,
                        }
                        return render(request, 'teacher/list_assignments.html',context)
                    except Teachers_Model.DoesNotExist:
                        return HttpResponseRedirect('login')
        else:
            return HttpResponseRedirect('login')



def teach_edit_assign(request):
    if 'UserName' in request.session:

                if request.method=="GET":
                    if request.GET.get('id'):
                        getDetails = Teachers_Model.objects.get(teach_UserName=request.session['UserName'])
                        print (getDetails)
                        assignmentData = Assignments.objects.filter(assignment_id=request.GET.get('id'))
                        print(assignmentData)
                       
                        context = {
                                'userName':getDetails.teach_UserName,
                                'assignmentData':assignmentData[0]
                            }

                        return render(request, 'teacher/edit_assignment.html',context)
                    else:
                        return HttpResponseRedirect('teach_lst_assignment?id=invalid')



                if request.method=="POST":
                    frm_assign_Last_Date = request.POST.get('assign_LastDate')
                    frm_assign_marks = request.POST.get('assgin_Marks')
                    frm_assign_QN = request.POST.get('assign_QN')
                    frm_assignment_status = request.POST.get('assignment_status')
                   
                    print('Assignment Updated Posted')
                    upDateStudent = Assignments.objects.filter(assignment_id=request.POST.get('id')).update(assignment_QN=frm_assign_QN, assignment_Marks=frm_assign_marks, assignment_Last_Date=frm_assign_Last_Date,assignment_status=frm_assignment_status)
                    print(upDateStudent)


                  
                    print('Assignment Details Update Succsesscull')
                    id=request.POST.get('id')
                    passValue='teach_edit_assignment?suc=updated'+'&id='+id
                    return HttpResponseRedirect(passValue)

          
    else:
            return HttpResponseRedirect('login')

      

def teach_del_assign(request):
    if 'UserName' in request.session:
        
            try:
                DeleteAssignment = Assignments.objects.get(assignment_id=request.GET.get('id'))
                DIR=DeleteAssignment.assignment_DIR

                # print(os.remove('assignments/'+DIR) 

                print(DeleteAssignment.delete())


                
                print("Assignment deleted successfully!")
                return HttpResponseRedirect('teach_lst_assignment?del=succ')

            except Exception as e:
                print(e)
                return HttpResponseRedirect('teach_lst_assignment?del=fail')

        
    else:
            return HttpResponseRedirect('login')   


def teach_view_assign(request):
    if 'UserName' in request.session:

                        getDetails = Teachers_Model.objects.get(teach_UserName=request.session['UserName'])
                        print (getDetails)
                        AssignmentListData = Assignemnt_Submissions.objects.all().select_related()
                        
                        context = {
                                'userName':getDetails.teach_UserName,
                                'AssignmentListData':AssignmentListData,
                        }
                        return render(request, 'teacher/view_assignments.html',context)
                    
    else:
        return HttpResponseRedirect('login')

def teach_view_assignment(request):

    if 'UserName' in request.session:

                if request.method=="GET":
                    if request.GET.get('id'):
                        getDetails = Teachers_Model.objects.get(teach_UserName=request.session['UserName'])
                        print (getDetails)
                        assignmentData = Assignemnt_Submissions.objects.filter(assignment_submittion_id=request.GET.get('id'))
                        if len(assignmentData)>0:

                            context = {
                                    'userName':getDetails.teach_UserName,
                                    'assignmentData':assignmentData[0]
                                }

                            return render(request, 'teacher/view_assignment.html', context)    
                        else:
                            return HttpResponseRedirect('teach_view_assignments?id=invalid')
                       
                    else:
                        return HttpResponseRedirect('teach_view_assignments?id=invalid')



                if request.method=="POST":
                    frm_assign_Last_Date = request.POST.get('assign_LastDate')
                    frm_assign_marks = request.POST.get('assgin_Marks')
                    frm_assign_QN = request.POST.get('assign_QN')
                    frm_assignment_status = request.POST.get('assignment_status')
                   
                    print('Assignment Updated Posted')
                    upDateStudent = Assignments.objects.filter(assignment_id=request.POST.get('id')).update(assignment_QN=frm_assign_QN, assignment_Marks=frm_assign_marks, assignment_Last_Date=frm_assign_Last_Date,assignment_status=frm_assignment_status)
                    print(upDateStudent)


                  
                    print('Assignment Details Update Succsesscull')
                    id=request.POST.get('id')
                    passValue='teach_view_assignment?suc=updated'+'&id='+id
                    return HttpResponseRedirect(passValue)

          
    else:
            return HttpResponseRedirect('login')




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


def process(request):

    if request.session.get('UserName'):
        return HttpResponseRedirect('teach_dashboard')
    if request.session.get('stdnt_usr'):
        return HttpResponseRedirect('stdnt_dash')
    else:
        return HttpResponseRedirect('login')



        



    
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




def handle_uploaded_file(file_passwd, file ):
    with open(file_passwd, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    print("file Uploaded")

# def download(request, path):
#     file_path = os.path.join(settings.MEDIA_ROOT, path)
#     if os.path.exists(file_path):
#         with open(file_path, 'rb') as fh:
#             response = HttpResponse(fh.read())
#             response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
#             return response
#     raise Http404
    
