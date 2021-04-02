from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .models import Task
from .forms import CreateTask


class IndexView(generic.ListView):
    template_name = 'todo/index.html'
    context_object_name = 'latest_todo_list'

    def get_queryset(self):
        """
        Return the last five created tasks that are not already completed
        """
        # QuerySet to retrieve objects
        return Task.objects.filter(
            completed__exact=False
        ).order_by('-creation_date')[:5]


class DetailView(generic.DetailView):
    model = Task
    template_name = 'todo/detail.html'


# TODO @login_required
def create_task(request):

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CreateTask(request.POST)  # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # save the form data to model
            form.save()
            # redirect to a new URL:
            return HttpResponseRedirect('confirmation/')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = CreateTask()
    return render(request, 'todo/create_task.html', {'form': form})


def confirmation_view(request):
    return HttpResponse()
