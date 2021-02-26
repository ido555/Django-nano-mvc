from django.http import HttpResponse


def index(request):
    return HttpResponse('<h2 style="text-align: center">Hey there</h2>')
