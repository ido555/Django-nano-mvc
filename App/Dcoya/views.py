from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, QueryDict
from http import HTTPStatus


def index(request):
    return HttpResponse('<h2 style="text-align: center">Index</h2>')


def registerClient(Request: WSGIRequest):
    if Request.POST is not None:
        data: QueryDict = Request.POST
        if 'username' in data.keys() and 'password' in data.keys():
            return HttpResponse('Mock Token')

    return HttpResponse(status=HTTPStatus.EXPECTATION_FAILED,
                        content="must include 'username' and 'password' parameters in a POST request")
