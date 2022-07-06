# Generated by Django 4.0.5 on 2022-07-06 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0003_alter_book_issue_model_book_issue_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance_model',
            fields=[
                ('attendance_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('attendance_added_by', models.CharField(max_length=50)),
                ('attendance_json_field', models.JSONField()),
                ('attendance_added_at', models.DateTimeField(auto_now_add=True)),
                ('attendance_update_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]