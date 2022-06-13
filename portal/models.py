from django.db import models


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
    fees_type=models.CharField(max_length=250)
    fees_amount=models.IntegerField(max_length=50)

    class Meta:
        db_table = "fees_tbl"


class Payments_Model(models.Model):
    payment_id = models.AutoField(primary_key=True)
    fees_type_id = models.CharField(max_length=50)
    fees_submited_Roll = models.CharField(max_length=50)
    fee_payment_mode= models.CharField(max_length=250)
    razorpay_payment_id = models.CharField(max_length=250)
    payment_state = models.BooleanField(default=True)
    payment_submittion_date = models.CharField(max_length=60)

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
    assignment_submittion_date = models.CharField(max_length=60)
    assignment_submittion_status = models.CharField(max_length=2)
    assignment_submittion_review = models.CharField(max_length=250)

    class Meta:
        db_table = "assignment_submittions"


class Notices(models.Model):
    notice_id = models.AutoField(primary_key=True)
    notice_Content = models.TextField()
    notice_issed_b = models.CharField(max_length=50)
    notice_issue_date = models.DateField(auto_now_add=True)

    class Meta:
        db_table = "notices"


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
