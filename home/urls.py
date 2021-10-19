from django.contrib import admin
from django.urls import path, include
from home import views


urlpatterns = [ 
    path('',views.index, name="home"),
    path('departments',views.dept, name="home"),
    # path('assignment_new',views.assignment_new, name="assignment_new"),
    # LOGINS VIEWS
   

    

]
