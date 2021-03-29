import datetime

from django.contrib.auth.models import AnonymousUser, User
from django.test import Client, TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model

from todo.models import Task


def create_task_simple(name, completed, created_by, days):
    """
    Create a task with the a 'name', 'completion status', 'author', and 'due_date' is the
    given number of `days` offset to now (negative for tasks due
    in the past, positive for tasks that are not yet due).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Task.objects.create(name=name, due_date=time, completed=completed,
                               created_by=created_by )


class TodoIndexViewTests(TestCase):
    def test_no_tasks(self):
        """
        If no tasks exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('todo:index'))
        self.assertEqual(response.status_code, 200)
        # checks the message "No tasks are available."
        self.assertContains(response, "No tasks are available.")
        # verify that latest_todo_list is empty
        self.assertQuerysetEqual(response.context['latest_todo_list'], [])

    def test_tasks(self):
        """
        Tasks are displayed on the index page.
        """
        # create user for testing
        self.user = User.objects.create_user(username='test_user', password='12345')
        create_task_simple(name="Task 1", days=-30, completed=False, created_by=self.user)
        response = self.client.get(reverse('todo:index'))
        self.assertQuerysetEqual(
            response.context['latest_todo_list'],
            ['<Task: Task 1>']
        )

    def test_completed_task(self):
        """
        Tasks that are already completed aren't displayed on
        the index page.
        """
        self.user = User.objects.create_user(username='test_user', password='12345')
        create_task_simple(name="Task 1", days=-30, completed=True, created_by=self.user)
        response = self.client.get(reverse('todo:index'))
        self.assertContains(response, "No tasks are available.")
        self.assertQuerysetEqual(response.context['latest_todo_list'], [])

    def test_two_tasks(self):
        """
        The to do index page may display multiple tasks.
        """
        self.user = User.objects.create_user(username='test_user', password='12345')
        create_task_simple(name="Task 1", days=-30, completed=False, created_by=self.user)
        create_task_simple(name="Task 2", days=-5, completed=False, created_by=self.user)
        response = self.client.get(reverse('todo:index'))
        self.assertQuerysetEqual(
            response.context['latest_todo_list'],
            ['<Task: Task 2>', '<Task: Task 1>']
        )

    def test_two_tasks_one_completed(self):
        """
        The index page will only show tasks that are not completed yet.
        """
        self.user = User.objects.create_user(username='test_user', password='12345')
        create_task_simple(name="Task 1", days=-30, completed=False, created_by=self.user)
        create_task_simple(name="Task 2", days=-5, completed=True, created_by=self.user)
        response = self.client.get(reverse('todo:index'))
        self.assertQuerysetEqual(
            response.context['latest_todo_list'],
            ['<Task: Task 1>']
        )
