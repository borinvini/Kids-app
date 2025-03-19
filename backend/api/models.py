from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Child(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    level = models.IntegerField(default=1)
    
    def __str__(self):
        return self.name

class Task(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE, related_name='tasks')
    task = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    money = models.DecimalField(max_digits=5, decimal_places=2)
    is_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.task