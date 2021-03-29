import datetime

from django.contrib.auth.models import AnonymousUser, User
from django.test import Client, TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model

from todo.models import Task


# TODO create test user if does not exist


def create_task_simple(name, completed, created_by, days):
    """
    Create a task with the a 'name', 'completion status', 'author', and 'due_date' is the
    given number of `days` offset to now (negative for tasks due
    in the past, positive for tasks that are not yet due).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Task.objects.create(name=name, due_date=time, completed=completed, created_by=created_by )


def create_task(
        name,
        task_list,
        creation_date,
        completed,
        completion_date,
        created_by,
        comments,
        days,):
    """
    Create a task with the a 'name', 'completion status', 'author', and 'due_date' is the
    given number of `days` offset to now (negative for tasks due
    in the past, positive for tasks that are not yet due).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Task.objects.create(
        name=name,
        task_list=task_list,
        creation_date=creation_date,
        due_date=time,
        completed=completed,
        completion_date=completion_date,
        created_by=created_by,
        comments=comments,)


class TaskModelOverDueStatusTests(TestCase):

    def test_completed_task_before_due_date_if(self):
        """
        create a task that was completed and is due in 30 days ago and
        check to see if the task is overdue
        """
        # create user for testing
        self.user = User.objects.create_user(username='test_user', password='12345')
        past_task = create_task_simple(name='task1', completed=True, created_by=self.user, days=30)
        self.assertIs(past_task.overdue_status(), False)

    def test_completed_task_past_due_date(self):
        """
        create a task that was due 30 ago and was completed to see if it is overdue
        """
        self.user = User.objects.create_user(username='test_user', password='12345')
        future_task = create_task_simple(name='task1', completed=True, created_by=self.user, days=-30)
        self.assertIs(future_task.overdue_status(), False)

    def test_not_completed_task_before_due_date(self):
        """
        create a task that is not completed and is due in 30 days and
        check to see if the task is overdue
        """
        self.user = User.objects.create_user(username='test_user', password='12345')
        past_task = create_task_simple(name='task1', completed=False, created_by=self.user, days=30)
        self.assertIs(past_task.overdue_status(), False)

    def test_not_completed_task_past_due_date(self):
        """
        create a task that was due 30 ago and not completed to see if it is overdue
        """
        self.user = User.objects.create_user(username='test_user', password='12345')
        future_task = create_task_simple(name='task1', completed=False, created_by=self.user, days=-30)
        self.assertIs(future_task.overdue_status(), True)
