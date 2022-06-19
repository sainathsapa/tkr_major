# Generated by Django 4.0.5 on 2022-06-19 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='accounts_usr',
            fields=[
                ('acc_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('acc_Name', models.CharField(max_length=50)),
                ('acc_Gender', models.BooleanField(default=False)),
                ('acc_Email', models.EmailField(max_length=254)),
                ('acc_Mobile', models.CharField(max_length=10)),
                ('acc_UserName', models.CharField(max_length=50)),
                ('acc_PWD', models.CharField(max_length=250)),
            ],
            options={
                'db_table': 'accounts_usr',
            },
        ),
        migrations.CreateModel(
            name='Admin_Model',
            fields=[
                ('admin_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('admin_usr_name', models.CharField(max_length=50)),
                ('admin_pwd', models.CharField(max_length=250)),
            ],
            options={
                'db_table': 'admin_tbl',
            },
        ),
        migrations.CreateModel(
            name='Assignemnt_Submissions',
            fields=[
                ('assignment_submittion_id', models.AutoField(primary_key=True, serialize=False)),
                ('assignment_Model_ID', models.CharField(max_length=50)),
                ('assignment_submited_Roll', models.CharField(max_length=50)),
                ('assignment_submited_Marks', models.CharField(max_length=50)),
                ('assignment_submitted_File', models.CharField(max_length=150)),
                ('assignment_submittion_date', models.DateTimeField(auto_now_add=True)),
                ('assignment_submittion_status', models.CharField(max_length=2)),
                ('assignment_submittion_review', models.CharField(max_length=250)),
            ],
            options={
                'db_table': 'assignment_submittions',
            },
        ),
        migrations.CreateModel(
            name='Assignments',
            fields=[
                ('assignment_id', models.AutoField(primary_key=True, serialize=False)),
                ('assignment_DIR', models.CharField(max_length=50)),
                ('assignment_QN', models.CharField(max_length=250)),
                ('assignment_Marks', models.CharField(max_length=50)),
                ('assignment_FileType', models.CharField(max_length=50)),
                ('assignment_Last_Date', models.CharField(max_length=50)),
                ('assignment_status', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'assignemnts',
            },
        ),
        migrations.CreateModel(
            name='Book_Issue_Model',
            fields=[
                ('book_issue_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('book_borrower_roll', models.CharField(max_length=50)),
                ('book_borrow_book_id', models.CharField(max_length=50)),
                ('book_borrow_requested_date', models.DateTimeField(auto_now_add=True)),
                ('book_issuer', models.CharField(max_length=50)),
                ('book_issue_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Books_Model',
            fields=[
                ('book_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('book_Name', models.CharField(max_length=50)),
                ('book_author', models.CharField(max_length=50)),
                ('book_img', models.CharField(max_length=500)),
                ('book_special_category', models.CharField(max_length=50)),
                ('book_desc', models.CharField(max_length=1000)),
                ('book_stock', models.IntegerField()),
                ('book_addedBy', models.CharField(max_length=50)),
                ('book_added_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Fees_Model',
            fields=[
                ('fees_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('fees_name', models.CharField(max_length=50)),
                ('fees_type', models.CharField(max_length=250)),
                ('fees_amount', models.IntegerField()),
            ],
            options={
                'db_table': 'fees_tbl',
            },
        ),
        migrations.CreateModel(
            name='Library_User_Model',
            fields=[
                ('lib_user_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('lib_userName', models.CharField(max_length=50)),
                ('lib_user_Gender', models.BooleanField(default=False)),
                ('lib_userEmail', models.CharField(max_length=50)),
                ('lib_user_FullName', models.CharField(max_length=50)),
                ('lib_user_pwd', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Notices_Model',
            fields=[
                ('notice_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('notice_added_user', models.CharField(max_length=50)),
                ('notice_issue_date', models.DateTimeField(auto_now_add=True)),
                ('notice_name', models.CharField(max_length=50)),
                ('notice_description', models.CharField(max_length=5000)),
            ],
            options={
                'db_table': 'notice_tbl',
            },
        ),
        migrations.CreateModel(
            name='Payments_Model',
            fields=[
                ('payment_id', models.AutoField(primary_key=True, serialize=False)),
                ('fees_type', models.CharField(max_length=50)),
                ('fees_submited_Roll', models.CharField(max_length=50)),
                ('razorpay_payment_id', models.CharField(max_length=250, null=True)),
                ('payment_state', models.BooleanField(default=True)),
                ('reason', models.CharField(max_length=255)),
                ('amount', models.CharField(max_length=255)),
                ('payment_submittion_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'payments_tbl',
            },
        ),
        migrations.CreateModel(
            name='Plagarized',
            fields=[
                ('plagarized_id', models.AutoField(primary_key=True, serialize=False)),
                ('plagarized_stdnt_one', models.CharField(max_length=50)),
                ('plagarized_stdnt_two', models.CharField(max_length=50)),
                ('plagarized_percentage', models.CharField(max_length=3)),
                ('plagarized_status', models.CharField(max_length=3)),
            ],
            options={
                'db_table': 'plagarized',
            },
        ),
        migrations.CreateModel(
            name='Students_Model',
            fields=[
                ('stdnt_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('stdnt_Name', models.CharField(max_length=50)),
                ('stdnt_Roll', models.CharField(max_length=50)),
                ('stdnt_Branch', models.CharField(max_length=50)),
                ('stdnt_DOB', models.CharField(max_length=50)),
                ('stdnt_Gender', models.BooleanField(default=False)),
                ('stdnt_Email', models.EmailField(max_length=254)),
                ('stdnt_Mobile', models.CharField(max_length=10)),
                ('stdnt_UserName', models.CharField(max_length=50)),
                ('stdnt_PWD', models.CharField(max_length=250)),
                ('stdnt_Total_Fees', models.CharField(max_length=50)),
                ('stdnt_is_Active', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'students_tbl',
            },
        ),
        migrations.CreateModel(
            name='Teachers_Model',
            fields=[
                ('tech_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('teach_Name', models.CharField(max_length=50)),
                ('tech_Gender', models.BooleanField(default=False)),
                ('teach_Email', models.EmailField(max_length=254)),
                ('teach_Mobile', models.CharField(max_length=10)),
                ('teach_UserName', models.CharField(max_length=50)),
                ('teach_PWD', models.CharField(max_length=250)),
            ],
            options={
                'db_table': 'teachers_tbl',
            },
        ),
    ]
