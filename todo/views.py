from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Task


class IndexView(generic.ListView):
    template_name = 'todo/index.html'
    context_object_name = 'latest_todo_list'

    def get_queryset(self):
        """
        Return the last five created tasks
        """
        return Task.objects.order_by('-due_date')[:5]


class DetailView(generic.DetailView):
    model = Task
    template_name = 'todo/detail.html'
