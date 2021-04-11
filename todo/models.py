import datetime

from django.conf import settings
from django.db import models
from django.db.models import UniqueConstraint
from django.utils import timezone
from django.contrib.auth.models import User

from django.contrib.auth import get_user_model


class TaskList(models.Model):

    """
    Model for the TaskLit allows for the grouping of individual tasks
    TODO documentation
    """
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,)

    class Meta:
        ordering = ['name']
        constraints = [
            # prevents the creation of tasklists with the same name for a given user at the database level
            # TODO Testing
            UniqueConstraint(fields=['user', 'name'], name='unique_user_tasklist'),
        ]

    def __str__(self):
        return self.name


class Task(models.Model):
    """
    Model that defines the Task relationships
    """
    name = models.CharField(max_length=100)
    task_list = models.ForeignKey(TaskList, on_delete=models.CASCADE, blank=True, null=True)
    creation_date = models.DateTimeField(default=timezone.now, blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    completed = models.BooleanField(default=False, blank=False)
    completion_date = models.DateTimeField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    comments = models.CharField(max_length=200, blank=True)

    class Priority (models.TextChoices):
        LOW = 'Low'
        MEDIUM = 'Medium'
        HIGH = 'High'

    priority = models.CharField(max_length=10, choices=Priority.choices)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    # Check if a task is currently overdue
    def overdue_status(self):

        # If a task is completed, it won't be overdue
        if self.completed:
            return False
        if self.due_date and timezone.now() > self.due_date:
            return True
        else:
            return False




