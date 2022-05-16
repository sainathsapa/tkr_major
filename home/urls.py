from django.contrib import admin
from django.urls import path, include
from home import views


urlpatterns = [ 
    path('',views.index, name="home"),
    path('departments',views.dept, name="dept"),
    path('placements',views.dept, name="placements"),
    path('about',views.dept, name="about"),
    path('contact',views.dept, name="contact"),
    # path('assignment_new',views.assignment_new, name="assignment_new"),
    # LOGINS VIEWS
   

    

]
