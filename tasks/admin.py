from django.contrib import admin

from .models import TaskList, Task, Attachment

admin.site.register(TaskList)
admin.site.register(Task)
admin.site.register(Attachment)
