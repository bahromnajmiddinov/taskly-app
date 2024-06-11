from rest_framework import serializers

from .models import House


class HouseSerializer(serializers.ModelSerializer): 
    members_count = serializers.IntegerField(read_only=True)
    members = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='profile-detail')
    manager = serializers.HyperlinkedRelatedField(read_only=True, many=False, view_name='profile-detail')
    tasklists = serializers.HyperlinkedRelatedField(read_only=True, many=True, view_name='tasklist-detail')
    
    class Meta:
        model = House
        fields = ['url', 'id', 'name', 'image', 'created', 
                  'manager', 'description', 'members_count', 'members', 'point', 
                  'completed_tasks_count', 'notcompleted_tasks_count', 'tasklists']
        read_only_fields = ['point', 'completed_tasks_count', 'notcompleted_tasks_count']
