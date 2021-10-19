from django.conf.urls import include
from django.urls import path
from django.views.generic import TemplateView
from portal import views



urlpatterns = [ 

    path('',views.process, name="LogIN"),  

    path('login',views.login, name="LogIN"),  
    path('logout',views.logout, name="LogOUT"),
    # path('download/(?P<path>.*',views.download, name="LogOUT"),

    
    # path('dirOpen',views.dirOpen, name="LogOUT"),

    path('teach_reg', views.reg_tech, name="Register Teacher"),    
    path('teach_dashboard', views.teach_dash, name="Teacher Dashboard"),
    path('teach_add_stdnt', views.teach_add_sdnt, name="Teacher Add Student"),
    path('teach_view_stdnt', views.teach_view_stdnt, name="Teacher View Student"),
    path('teach_edit_stdnt', views.teach_edit_stdnt, name="Teacher Edit Student"),
    path('teach_del_stdnt', views.teach_del_stdnt, name="Teacher Student Delete"),
    path('teach_nw_assignment', views.teach_nw_assign, name="Teacher New Assgignment"),
    path('teach_lst_assignment', views.teach_lst_assign, name="Teacher List Assignment"),
    path('teach_edit_assignment', views.teach_edit_assign, name="Teacher Edit Assignment"),
    path('teach_del_assignment', views.teach_del_assign, name="Teacher Delete Assignment"),
    path('teach_view_assignments', views.teach_view_assign, name="Teacher View Assignments"),
    path('teach_view_assignment', views.teach_view_assignment, name="Teacher View Assignments"),




    path('stdnt_dash', views.stdnt_dash, name="Student Dashboard"),
    path('stdnt_nw_assignment', views.stdnt_nw_assignment, name="Student Dashboard"),    
    path('stdnt_upload_assignment', views.stdnt_upload_assignment, name="Student Dashboard"),
    path('stdnt_view_assignments', views.stdnt_view_assignments, name="Student Dashboard"),




    
]
