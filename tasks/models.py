import uuid
import os

from django.db import models
from django.utils.deconstruct import deconstructible

from users.models import Profile
from house.models import House


@deconstructible
class GenerateTaskAttachmentPath(object):
    def __init__(self):
        pass
    
    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        path = f'media/tasks/{instance.task.id}/attachments/'
        name = f'{instance.id}.{ext}'
        return os.path.join(path, name)


task_attachment_path = GenerateTaskAttachmentPath()


NOT_COMPLETED = 'NOT'
COMPLETED = 'COM'
TASK_STATUS_CHOICES = (
    (NOT_COMPLETED, 'Not Completed'),
    (COMPLETED, 'Completed'),
)


class TaskList(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    completed = models.DateTimeField(null=True, blank=True)
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='tasklists')
    created_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True, related_name='tasklist_owners')
    name = models.CharField(max_length=120)
    description = models.TextField()
    status = models.CharField(max_length=3, choices=TASK_STATUS_CHOICES, default=NOT_COMPLETED)
    
    def __str__(self):
        return self.name
    
    

class Task(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    completed = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True, related_name='created_tasks')
    completed_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, blank=True, null=True, related_name='completed_tasks')
    task_list = models.ForeignKey(TaskList, on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=120)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=3, choices=TASK_STATUS_CHOICES, default=NOT_COMPLETED)
    
    def __str__(self):
        return self.name
    

class Attachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    data = models.FileField(upload_to=task_attachment_path)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='attachments')
    
    def __str__(self):
        return f'{self.id} | {self.task}'
