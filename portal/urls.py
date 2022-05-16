from django.conf.urls import include
from django.urls import path
from django.views.generic import TemplateView
from portal import views
from portal import students
from portal import teach



urlpatterns = [ 

    path('',views.process, name="LogIN"),  

    path('login',views.login, name="LogIN"),  
    path('logout',views.logout, name="LogOUT"),
    # path('download/(?P<path>.*',views.download, name="LogOUT"),

    
    # path('dirOpen',views.dirOpen, name="LogOUT"),

    path('teach_reg', views.reg_tech, name="Register Teacher"),

    # Teacher Modules
    path('teach_dashboard', teach.teach_dash, name="Teacher Dashboard"),
    path('teach_add_stdnt', teach.teach_add_sdnt, name="Teacher Add Student"),
    path('teach_view_stdnt', teach.teach_view_stdnt, name="Teacher View Student"),
    path('teach_edit_stdnt', teach.teach_edit_stdnt, name="Teacher Edit Student"),
    path('teach_del_stdnt', teach.teach_del_stdnt, name="Teacher Student Delete"),
    path('teach_nw_assignment', teach.teach_nw_assign, name="Teacher New Assgignment"),
    path('teach_lst_assignment', teach.teach_lst_assign, name="Teacher List Assignment"),
    path('teach_edit_assignment', teach.teach_edit_assign, name="Teacher Edit Assignment"),
    path('teach_del_assignment', teach.teach_del_assign, name="Teacher Delete Assignment"),
    # path('teach_view_assignments', teach.teach_view_assign, name="Teacher View Assignments"),
    path('teach_view_assignment', teach.teach_view_assignment, name="Teacher View Assignments"),
    path('teach_view_submitted_assignments', teach.teach_view_submitted_assignments, name="Teacher View Assignments"),


    # Stdent Modules

    path('stdnt_dash', students.stdnt_dash, name="Student Dashboard"),
    path('stdnt_nw_assignment', students.stdnt_nw_assignment, name="Student Dashboard"),    
    path('stdnt_upload_assignment', students.stdnt_upload_assignment, name="Student Upload Assignment"),
    path('stdnt_view_assignments', students.stdnt_view_assignments, name="Student View Assignt"),
    path('stdnt_del_assignment', students.stdnt_del_assignment, name="Student View Assignt"),
    path('stdnt_re_upload_assignment', students.stdnt_re_upload_assignment, name="Student View Assignt"),




    
]
