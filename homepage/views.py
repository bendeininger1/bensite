from django.http import HttpResponse


# home page
def home(request):
    return HttpResponse('<em>Home Page</em>')