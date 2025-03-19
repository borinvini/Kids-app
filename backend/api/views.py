from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Task, Child
from .serializers import TaskSerializer, ChildSerializer

# Create your views here.
class ChildViewSet(viewsets.ModelViewSet):
    queryset = Child.objects.all()
    serializer_class = ChildSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # User can only view their own children
        return Child.objects.filter(user=self.request.user)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Filter tasks by child_id if provided
        child_id = self.request.query_params.get('child_id')
        if child_id:
            return Task.objects.filter(child_id=child_id)
        # Otherwise return tasks for all of the user's children
        return Task.objects.filter(child__user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def toggle_complete(self, request, pk=None):
        task = self.get_object()
        task.is_complete = not task.is_complete
        
        if task.is_complete:
            task.completed_at = timezone.now()
        else:
            task.completed_at = None
            
        task.save()
        return Response({'status': 'task updated', 'is_complete': task.is_complete})