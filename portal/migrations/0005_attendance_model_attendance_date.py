# Generated by Django 4.0.5 on 2022-07-06 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0004_attendance_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance_model',
            name='attendance_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
