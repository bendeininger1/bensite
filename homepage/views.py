from django.shortcuts import render
from django.http import HttpResponse


# home page
def home(request):
    return render(request, 'homepage/homepage.html', {'insert_me': 'Hello this is a test'})
    # return HttpResponse('<em>Home Page</em>')


def help_page(request):
    return render(request, 'homepage/help.html', {'help_insert': 'Help Page'})
