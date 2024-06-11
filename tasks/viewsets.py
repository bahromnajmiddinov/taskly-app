from django.utils import timezone

from rest_framework import viewsets, mixins, filters
from rest_framework import status as s
from rest_framework.decorators import action
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend

from .serializers import TaskListSerializer, TaskSerializer, AttachmentSerializer
from .models import TaskList, Task, Attachment, COMPLETED, NOT_COMPLETED
from .permissions import IsAllowedToEditTaskListElseNone, IsAllowedToEditTaskElseNone, IsAllowedToEditAttchmentElseNone


class TaskListViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAllowedToEditTaskListElseNone]
    queryset = TaskList.objects.all()
    serializer_class = TaskListSerializer
    
    def get_queryset(self):
        queryset = super(TaskListViewSet, self).get_queryset()
        user_profile = self.request.user
        updated_queryset = queryset.filter(created_by=user_profile)
        return updated_queryset
    

class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAllowedToEditTaskElseNone]
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'description',]
    filterset_fields = ['status',]
    
    @action(detail=True, methods=['patch'])
    def update_task_status(self, request, pk=None):
        try:
            task = self.get_object()
            user_profile = request.user
            status = request.data['status']
            
            if status == NOT_COMPLETED:
                if task.status == COMPLETED:
                    task.status = NOT_COMPLETED
                    task.completed = None
                    task.completed_by = None
                else:
                    raise Exception('Task is already Completed')
            elif status == COMPLETED:
                if task.status == NOT_COMPLETED:
                    task.status = COMPLETED
                    task.completed = timezone.now()
                    task.completed_by = user_profile
                else:
                    raise Exception('Task is already Completed')
            else:
                raise Exception('Incorrect status provided')
            task.save()
            serializer = TaskSerializer(instance=task, context={'request': request})
            return Response(serializer.data, status=s.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=s.HTTP_404_BAD_REQUEST)
        

class AttachmentViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAllowedToEditAttchmentElseNone]
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer
