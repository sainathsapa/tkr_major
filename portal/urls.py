from django.conf.urls import include
from django.urls import path
from django.views.generic import TemplateView
from portal import accounts, views
from portal import students
from portal import teach
from portal import library


urlpatterns = [

    path('', views.process, name="LogIN"),

    path('login', views.login, name="LogIN"),
    path('logout', views.logout, name="LogOUT"),
    # path('download/(?P<path>.*',views.download, name="LogOUT"),


    # path('dirOpen',views.dirOpen, name="LogOUT"),

    path('teach_reg', views.reg_tech, name="Register Teacher"),

    # Teacher Modules
    path('teach_dashboard', teach.teach_dash, name="Teacher Dashboard"),
    path('teach_add_stdnt', teach.teach_add_sdnt, name="Teacher Add Student"),
    path('teach_view_stdnt', teach.teach_view_stdnt, name="Teacher View Student"),
    path('teach_edit_stdnt', teach.teach_edit_stdnt, name="Teacher Edit Student"),
    path('teach_del_stdnt', teach.teach_del_stdnt,
         name="Teacher Student Delete"),
    path('teach_nw_assignment', teach.teach_nw_assign,
         name="Teacher New Assgignment"),
    path('teach_lst_assignment', teach.teach_lst_assign,
         name="Teacher List Assignment"),
    path('teach_edit_assignment', teach.teach_edit_assign,
         name="Teacher Edit Assignment"),
    path('teach_del_assignment', teach.teach_del_assign,
         name="Teacher Delete Assignment"),
    # path('teach_view_assignments', teach.teach_view_assign, name="Teacher View Assignments"),
    path('teach_view_assignment', teach.teach_view_assignment,
         name="Teacher View Assignments"),
    path('teach_view_submitted_assignments',
         teach.teach_view_submitted_assignments, name="Teacher View Assignments"),


    # Stdent Modules

    path('stdnt_dash', students.stdnt_dash, name="Student Dashboard"),
    path('stdnt_profile', students.stdnt_profile, name="stdnt_profile"),
    path('stdnt_nw_assignment', students.stdnt_nw_assignment,
         name="Student Dashboard"),
    path('stdnt_upload_assignment', students.stdnt_upload_assignment,
         name="Student Upload Assignment"),
    path('stdnt_view_assignments', students.stdnt_view_assignments,
         name="Student View Assignt"),
    path('stdnt_del_assignment', students.stdnt_del_assignment,
         name="Student View Assignt"),
    path('stdnt_re_upload_assignment',
         students.stdnt_re_upload_assignment, name="Student View Assignt"),
    path('stdnt_nw_payment', students.stdnt_nw_payment,
         name="Student New Payment"),
    path('stdnt_indvid_mk_payment', students.stdnt_indvid_mk_payment,
         name="Student New Payment"),
    path('stdnt_view_payments', students.stdnt_view_payments,
         name="Student View Payments"),

    path('stdnt_view_notices', students.stdnt_view_notices,
         name="Student View Notices"),
    path('stdnt_view_notice', students.stdnt_view_notice,
         name="Student View Notices"),
    path('stdnt_new_borrow_req', students.stdnt_new_borrow_req,
         name="Student View Books"),
    path('stdnt_view_book', students.stdnt_view_book,
         name="Student View Book"),
    path('posted_book_borrow_req', students.posted_book_borrow_req,
         name="Student Add Req Book"),

    path('stdnt_lib_pending_books', students.stdnt_lib_pending_books,
         name="Student View Book"),
    path('stdnt_del_borrow_req', students.stdnt_del_borrow_req,
         name="Student View Book"),



    # Accounts Module
    path('acc_dashboard', accounts.acc_dashboard, name="Account Dashboard"),
    path('acc_view_stdnt', accounts.acc_view_stdnt, name="Account View Student"),
    path('acc_add_payment_type', accounts.acc_add_payment_type,
         name="Account Add Payment Method"),
    path('acc_view_payment_types', accounts.acc_view_payment_types,
         name="Account View Payment Method"),

    path('acc_del_payment_method', accounts.acc_del_payment_method,
         name="Account Delete Payment Method"),
    path('acc_view_payments', accounts.acc_view_payments,
         name="Account View Payments"),
    path('acc_stdnt_view_payments', accounts.acc_sdnt_view_payments,
         name="Account STDNT View Payments"),
    path('acc_add_notice', accounts.acc_add_notices,
         name="Account Add Notice"),
    path('acc_view_notices', accounts.acc_view_notices,
         name="Account View Notices"),
    path('acc_view_notice', accounts.acc_view_notice,
         name="Account View Notices"),


    # Library Model
    path('lib_dashboard', library.lib_dashboard, name="Library Dashboard"),
    path('lib_view_stdnts', library.lib_view_stdnts,
         name="Library View Students"),

    path('lib_add_new_book', library.lib_add_new_book, name="Library Add Book"),
    path('lib_view_books', library.lib_view_books, name="Library View Book"),
    path('lib_edit_book', library.lib_edit_book, name="Library Edit Book"),
    path('lib_del_book', library.lib_del_book, name="Library Delete Book"),
    path('lib_view_borrow_req', library.lib_view_borrow_req,
         name="Library Pending Issue Book"),
    path('lib_del_borrow_req', library.lib_del_borrow_req,
         name="Library Pending Issue Book"),
    path('lib_view_specific_book_req', library.lib_view_specific_book_req,
         name="Library Pending Issue Book"),
    path('lib_update_book_rq', library.lib_update_book_rq,
         name="Library Pending Issue Book"),

    path('lib_add_notice', library.lib_add_notices,
         name="library Add Notice"),
    path('lib_view_notices', library.lib_view_notices,
         name="library View Notices"),
    path('lib_view_notice', library.lib_view_notice,
         name="library View Notices"),
    path('lib_book_issues', library.lib_book_issues,
         name="library View Book Issues"),
    path('lib_pending_books', library.lib_pending_books,
         name="library View Pending Books"),
    path('lib_stdnt_view_books', library.lib_stdnt_view_books,
         name="library Student Book Borrow Notices"),
    path('lib_profile', library.lib_profile,
         name="library Profile")





]
