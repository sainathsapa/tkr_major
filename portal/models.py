from statistics import mode
from this import d
from django.db import models
from django.contrib.postgres.fields import JSONField
# from django.utils.translation import gettext_lazy as _



class Students_Model(models.Model):
    stdnt_id = models.BigAutoField(primary_key=True)
    stdnt_Name = models.CharField(max_length=50)
    stdnt_Roll = models.CharField(max_length=50)
    stdnt_Branch = models.CharField(max_length=50)
    stdnt_DOB = models.CharField(max_length=50)
    stdnt_Gender = models.BooleanField(default=False)
    stdnt_Email = models.EmailField(max_length=254)
    stdnt_Mobile = models.CharField(max_length=10)
    stdnt_UserName = models.CharField(max_length=50)
    stdnt_PWD = models.CharField(max_length=250)
    stdnt_Total_Fees = models.CharField(max_length=50)
    stdnt_is_Active = models.BooleanField(default=False)

    class Meta:
        db_table = "students_tbl"


class Fees_Model(models.Model):
    fees_id = models.BigAutoField(primary_key=True)
    fees_name = models.CharField(max_length=50)
    fees_type = models.CharField(max_length=250)
    fees_amount = models.IntegerField()

    class Meta:
        db_table = "fees_tbl"


class Payments_Model(models.Model):
    payment_id = models.AutoField(primary_key=True)
    fees_type = models.CharField(max_length=50)
    fees_submited_Roll = models.CharField(max_length=50)
    razorpay_payment_id = models.CharField(max_length=250, null=True)
    payment_state = models.BooleanField(default=True)
    reason = models.CharField(max_length=255)
    amount = models.CharField(max_length=255)
    payment_submittion_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "payments_tbl"


class Teachers_Model(models.Model):
    tech_id = models.BigAutoField(primary_key=True)
    teach_Name = models.CharField(max_length=50)
    tech_Gender = models.BooleanField(default=False)
    teach_Email = models.EmailField(max_length=254)
    teach_Mobile = models.CharField(max_length=10)
    teach_UserName = models.CharField(max_length=50)
    teach_PWD = models.CharField(max_length=250)

    class Meta:
        db_table = "teachers_tbl"


class Assignments(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    assignment_DIR = models.CharField(max_length=50)
    assignment_QN = models.CharField(max_length=250)
    assignment_Marks = models.CharField(max_length=50)
    assignment_FileType = models.CharField(max_length=50)

    assignment_Last_Date = models.CharField(max_length=50)
    assignment_status = models.BooleanField(default=False)

    class Meta:
        db_table = "assignemnts"


class Admin_Model(models.Model):
    admin_id = models.BigAutoField(primary_key=True)
    admin_usr_name = models.CharField(max_length=50)
    admin_pwd = models.CharField(max_length=250)

    class Meta:
        db_table = "admin_tbl"


class Assignemnt_Submissions(models.Model):
    assignment_submittion_id = models.AutoField(primary_key=True)
    assignment_Model_ID = models.CharField(max_length=50)
    assignment_submited_Roll = models.CharField(max_length=50)
    assignment_submited_Marks = models.CharField(max_length=50)
    assignment_submitted_File = models.CharField(max_length=150)
    assignment_submittion_date = models.DateTimeField(auto_now_add=True)
    assignment_submittion_status = models.CharField(max_length=2)
    assignment_submittion_review = models.CharField(max_length=250)

    class Meta:
        db_table = "assignment_submittions"


class Plagarized(models.Model):

    plagarized_id = models.AutoField(primary_key=True)
    plagarized_stdnt_one = models.CharField(max_length=50)
    plagarized_stdnt_two = models.CharField(max_length=50)
    plagarized_percentage = models.CharField(max_length=3)
    plagarized_status = models.CharField(max_length=3)

    class Meta:
        db_table = "plagarized"


class accounts_usr(models.Model):
    acc_id = models.BigAutoField(primary_key=True)
    acc_Name = models.CharField(max_length=50)
    acc_Gender = models.BooleanField(default=False)
    acc_Email = models.EmailField(max_length=254)
    acc_Mobile = models.CharField(max_length=10)
    acc_UserName = models.CharField(max_length=50)
    acc_PWD = models.CharField(max_length=250)

    class Meta:
        db_table = "accounts_usr"


class Notices_Model(models.Model):
    notice_id = models.BigAutoField(primary_key=True)
    notice_added_user = models.CharField(max_length=50)
    notice_issue_date = models.DateTimeField(auto_now_add=True)
    notice_name = models.CharField(max_length=50)
    notice_description = models.CharField(max_length=5000)

    class Meta:
        db_table = "notice_tbl"


class Library_User_Model(models.Model):
    lib_user_id = models.BigAutoField(primary_key=True)
    lib_userName = models.CharField(max_length=50)
    lib_user_Gender = models.BooleanField(default=False)
    lib_userEmail = models.CharField(max_length=50)
    lib_user_FullName = models.CharField(max_length=50)
    lib_user_pwd = models.CharField(max_length=250)

    class metadata:
        db_table = "library_user_tbl"


class Books_Model(models.Model):
    book_id = models.BigAutoField(primary_key=True)
    book_Name = models.CharField(max_length=50)
    book_author = models.CharField(max_length=50)
    book_img = models.CharField(max_length=500)
    book_special_category = models.CharField(max_length=50)
    book_desc = models.CharField(max_length=1000)
    book_stock = models.IntegerField()
    book_addedBy = models.CharField(max_length=50)
    book_added_date = models.DateTimeField(auto_now_add=True)

    class metadata:
        db_table = "books_tbl"


class Book_Issue_Model(models.Model):
    book_issue_id = models.BigAutoField(primary_key=True)
    book_borrower_roll = models.CharField(max_length=50)
    book_borrow_book_id = models.CharField(max_length=50)
    book_borrow_requested_date = models.DateTimeField(auto_now_add=True)
    book_issuer = models.CharField(max_length=50)
    book_issue_date = models.DateTimeField(null=True, blank=True)
    book_issue_state = models.CharField(max_length=50)

class Attendance_model(models.Model):
    attendance_id= models.BigAutoField(primary_key=True)
    attendance_added_by= models.CharField(max_length=50)
    attendance_date=models.DateField(null=True, blank=True)
    attendance_json_field= models.JSONField()
    attendance_added_at=models.DateTimeField(auto_now_add=True)
    attendance_update_at= models.DateTimeField(auto_now=True)
    
