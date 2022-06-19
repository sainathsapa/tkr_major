# Generated by Django 4.0.5 on 2022-06-19 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book_issue_model',
            name='book_issue_state',
            field=models.CharField(default=0, max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='book_issue_model',
            name='book_issue_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
