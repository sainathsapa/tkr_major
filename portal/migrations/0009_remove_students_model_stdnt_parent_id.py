# Generated by Django 4.0.5 on 2022-07-07 02:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0008_students_model_stdnt_parent_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='students_model',
            name='stdnt_Parent_id',
        ),
    ]