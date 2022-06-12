from django.contrib import admin
from portal.models import Students_Model, Teachers_Model, Assignments, Assignemnt_Submissions, Notices, Plagarized, Fees_Model, accounts_usr, Payments_Model
# Register your models here.
admin.site.register(Students_Model)
admin.site.register(Teachers_Model)
admin.site.register(Assignments)
admin.site.register(Assignemnt_Submissions)
admin.site.register(Notices)
admin.site.register(Plagarized)
admin.site.register(accounts_usr)
admin.site.register(Fees_Model)
admin.site.register(Payments_Model)
