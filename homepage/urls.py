from django.urls import path

from . import views

app_name = 'homepage'
urlpatterns = [
    # homepage
    path('', views.home, name='home'),
    # help page
    path('help/', views.help_page, name='help'),
]
