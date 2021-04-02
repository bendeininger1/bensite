from django import forms
from django.contrib.auth.models import Group
from django.forms import ModelForm, SelectDateWidget
from django.utils import timezone

from todo.models import Task, TaskList


# TODO forms.Form or ModelForm (and import ModelForm)
class CreateTask(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'due_date', 'completed', 'comments']
        widgets = {
            'due_date': SelectDateWidget()
        }
