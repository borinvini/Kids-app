from django.contrib import admin
from .models import Task, Child

# Register your models here.
@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'user')
    search_fields = ('name',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('task', 'child', 'money', 'is_complete', 'created_at')
    list_filter = ('is_complete', 'child')
    search_fields = ('task', 'description')