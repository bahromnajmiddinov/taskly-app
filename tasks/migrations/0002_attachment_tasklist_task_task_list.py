# Generated by Django 5.0.6 on 2024-06-10 07:32

import django.db.models.deletion
import tasks.models
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('house', '0001_initial'),
        ('tasks', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('data', models.FileField(upload_to=tasks.models.GenerateTaskAttachmentPath())),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='tasks.task')),
            ],
        ),
        migrations.CreateModel(
            name='TaskList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('completed', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=120)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('NOT', 'Not Completed'), ('COM', 'Completed')], default='NOT', max_length=3)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tasklist_owners', to=settings.AUTH_USER_MODEL)),
                ('house', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasklists', to='house.house')),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='task_list',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='tasks.tasklist'),
            preserve_default=False,
        ),
    ]
