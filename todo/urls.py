from django.urls import path

from . import views

app_name = 'todo'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # allows users to see the list of tasks that are not yet complete
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # allows users to create new tasks
    path('create_task/', views.create_task, name='create_task'),
    # form submission confirmation page
    path('create_task/confirmation/', views.confirmation_view)
]
