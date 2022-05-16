from django.contrib import admin
from portal.models import Students_Model,Teachers_Model, Assignments, Assignemnt_Submissions, Notices, Plagarized
# Register your models here.
admin.site.register(Students_Model)
admin.site.register(Teachers_Model)
admin.site.register(Assignments)
admin.site.register(Assignemnt_Submissions)
admin.site.register(Notices)
admin.site.register(Plagarized)

