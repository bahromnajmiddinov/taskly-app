from rest_framework import serializers

from .models import TaskList, Task, Attachment
from house.models import House


class TaskListSerializer(serializers.ModelSerializer):
    house = serializers.HyperlinkedRelatedField(queryset=House.objects.all(), many=False, view_name='house-detail')
    created_by = serializers.HyperlinkedRelatedField(read_only=True, many=False, view_name='profile-detail')
    tasks = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='task-detail')
    
    class Meta:
        model = TaskList
        fields = ['url', 'id', 'name', 'description', 'status', 'created', 'completed', 'house', 'created_by', 'tasks']
        read_only_fields = ['created', 'status']


class TaskSerializer(serializers.ModelSerializer):
    created_by = serializers.HyperlinkedRelatedField(read_only=True, many=False, view_name='profile-detail')
    completed_by = serializers.HyperlinkedRelatedField(read_only=True, many=False, view_name='profile-detail')
    task_list = serializers.HyperlinkedRelatedField(queryset=TaskList.objects.all(), many=False, view_name='tasklist-detail')
    attachments = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='attachment-detail')
    
    class Meta:
        model = Task
        fields = ['url', 'id', 'name', 'description', 'status', 'created', 'completed', 'created_by', 'completed_by', 'task_list', 'attachments']
        read_only_fields = ['created', 'created_by', 'completed', 'completed_by', 'status']
        
    def validate_task_list(self, value):
        user_profile = self.context['request'].user
        if value not in user_profile.house.tasklists.all():
            raise serializers.ValidationError({'TaskList': 'Tasklist provided does not belong to house for which user is member'})
        return value
    
    def create(self, validated_data):
        user_profile = self.context['request'].user
        task = Task.objects.create(**validated_data)
        task.created_by = user_profile
        task.save()
        return task


class AttachmentSerializer(serializers.ModelSerializer):
    task = serializers.HyperlinkedRelatedField(queryset=Task.objects.all(), many=False, view_name='task-detail')
    
    class Meta:
        model = Attachment
        fields = ['url', 'id', 'created', 'task', 'data']
        read_only_fields = ['created']
        
    def validate(self, attrs):
        user_profile = self.context['request'].user
        task = attrs['task']
        task_list = TaskList.objects.get(tasks__id__exact=task.id)
        if task_list not in user_profile.house.tasklists.all():
            raise seriazilers.ValidationError({'Task': 'Task provided does not belong to house for which user is member'})
        return attrs
