import os
from django.conf import settings
from django.db.models.query import QuerySet

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
                        plag(AssignmentListData[1].assignment_DIR, AssignmentListData[1].assignment_FileType)
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

def teach_view_assignment(request):

    if 'UserName' in request.session:

                if request.method=="GET":
                    if request.GET.get('id'):
                        getDetails = Teachers_Model.objects.get(teach_UserName=request.session['UserName'])
                        print (getDetails)
                        assignmentData = Assignemnt_Submissions.objects.filter(assignment_submittion_id=request.GET.get('id'))
                        studentData = Students_Model.objects.filter(stdnt_Roll=assignmentData[0].assignment_submited_Roll)
                        print(studentData[0])

                        if len(assignmentData)>0:

                            context = {
                                    'userName':getDetails.teach_UserName,
                                    'assignmentData':assignmentData[0],
                                    'studentData':studentData[0]
                                }

                            return render(request, 'teacher/view_assignment.html', context)    
                        else:
                            return HttpResponseRedirect('teach_view_assignments?id=invalid')
                       
                    else:
                        return HttpResponseRedirect('teach_view_assignments?id=invalid')



                if request.method=="POST":
                    frm_review = request.POST.get('review_frm')
                    frm_marks = request.POST.get('stdnt_assignMarks')
                    frm_status = request.POST.get('status_frm')
                    
                   
                    print('Assignment Updated Posted')
                    upDateStudent = Assignemnt_Submissions.objects.filter(assignment_submittion_id=request.POST.get('id')).update(assignment_submited_Marks=frm_marks, assignment_submittion_status=frm_status, assignment_submittion_review=frm_review)
                    print(upDateStudent)


                  
                    print('Assignment Details Update Succsesscull')
                    id=request.POST.get('id')
                    passValue='teach_view_assignment?suc=updated'+'&id='+id
                    return HttpResponseRedirect(passValue)

          
    else:
            return HttpResponseRedirect('login')




def teach_view_submitted_assignments(request):
    if 'UserName' in request.session:
                    if request.GET.get('id'):

                        getDetails = Teachers_Model.objects.get(teach_UserName=request.session['UserName'])
                        # print (getDetails)
                        
                        AssignmentListData = Assignemnt_Submissions.objects.filter(assignment_Model_ID=request.GET.get('id'))
                        
                        AssignmentDirVar = Assignments.objects.filter(assignment_id=request.GET.get('id'))
                        # print(AssignmentDirVar[0].assignment_FileType)
                        Matched_Content=plag(AssignmentDirVar[0].assignment_DIR, AssignmentDirVar[0].assignment_FileType)
                        # print(type(Matched_Content[0][0]))
                        # AssignmentListData.extra(Matched_Content)

                    
                        context = {
                                'userName':getDetails.teach_UserName,
                                'AssignmentListData':AssignmentListData,
                                'Matched_Content':Matched_Content
                        }
                        
                        return render(request, 'teacher/view_assignments.html',context)
                    else :
                        return HttpResponseRedirect('teach_lst_assignment')

                    
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

    
def plag(PassDir, PassType):
    dir="assignments/"+PassDir
    fileType=PassType    
    studnt_Submitted_Files = [doc for doc in os.listdir(dir) if doc.endswith(fileType)]
    studnt_Submitted_Files_DT =[open(dir+"/"+File).read() for File in  studnt_Submitted_Files]


    # Getting Data from FIles
    vectorize = lambda Text: TfidfVectorizer().fit_transform(Text).toarray()

    # Findinnging Similarity
    similarity = lambda doc1, doc2: cosine_similarity([doc1, doc2])
    # creating a array
    vectors = vectorize(studnt_Submitted_Files_DT)
    s_vector = list(zip(studnt_Submitted_Files, vectors))

    # Similarity Checking Function
    def check_plagiarism():
        # s_vectors = list(zip(studnt_Submitted_Files, vectors))

        plagiarism_results = []
        

        for student_a, text_vector_a in s_vector:
            new_vectors =s_vector.copy()
            current_index = new_vectors.index((student_a, text_vector_a))
            del new_vectors[current_index]
            for student_b , text_vector_b in new_vectors:
                sim_score = similarity(text_vector_a, text_vector_b)[0][1] * 100
                
                student_pair = sorted((student_a, student_b))
                score = dict()
                score['P1'] = student_pair[0]
                score['P2']= student_pair[1]
                score['score'] = sim_score
                plagiarism_results.append(score)
        return plagiarism_results
    QuerytoReturn=[]    
    for data in check_plagiarism():
        QuerytoReturn.append(data)
    return QuerytoReturn
    