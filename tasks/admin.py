from django.contrib import admin
from .models import Task, Comment, Team,  FileAttachment


# Register your models here.
admin.site.register(Task)
admin.site.register(Comment)
admin.site.register(FileAttachment)
admin.site.register(Team)