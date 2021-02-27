from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from http import HTTPStatus
from json import loads as jsonLoads
from .models import User
from django.db.models.manager import Manager, QuerySet
from django.db.utils import Error
from App.App.settings import SECRET_KEY
from jwt import encode, decode

def index(request):
    return HttpResponse('<h2 style="text-align: center">Index</h2>')


def registerClient(request: WSGIRequest):
    if request.method == "POST":
        data: dict = jsonLoads(request.body)
        if len(data.keys()) != 2:
            return HttpResponse(status=HTTPStatus.EXPECTATION_FAILED,
                                content="must include only 2 parameters: 'username' and 'password' in a JSON format")

        for k, v in data.items():
            if k == "username" or "password":
                if len(v) > 255:
                    return HttpResponse(status=HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
                                        content="each JSON parameter should not exceed 255 characters in size")
            # passed checks - create model and return token
        try:
            if isUsernameExists(data.get('username')):
                return HttpResponse(status=HTTPStatus.CONFLICT, content="This username is taken")
            insertUser(data.get('username'), data.get('password'))
        except Error:
            return HttpResponse(HTTPStatus.INTERNAL_SERVER_ERROR, 'Something went  wrong, please try again later')

        return HttpResponse('Mock Token')
    return HttpResponse(status=HTTPStatus.EXPECTATION_FAILED,
                        content="Must include 'username' and 'password' in a POST request's body in a JSON format")


def isUsernameExists(username: str):
    try:
        return QuerySet(model=User).all().filter(username=username).exists()
    except Error as e:
        raise str(e)


def insertUser(username: str, password: str):
    try:
        encode({"some": "payload"}, "secret", algorithm="HS256")
        user: User = User()
        user.username = username
        user.password = password
        user.save()
    except Error as e:
        raise str(e)
