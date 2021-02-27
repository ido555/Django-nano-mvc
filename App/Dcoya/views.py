from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from http import HTTPStatus
from json import loads as jsonLoads
from .models import User
from django.db.models.manager import Manager, QuerySet
from django.db.utils import Error
from jwt import encode, decode, PyJWTError

secretiveSecret = "fpj2u6fCLsHeb6TjuvFBC9ULNmpN4xC9qW6Cz57wU969jzpEA2mPaCvb2rmwpXZXpTVWEShM4S75ysjeB3wBU3Y9QSQQu2SvwQqj5jWRMH5FWQCDCgAQuFWTdwPSKVXN"


def registerClient(request: WSGIRequest):
    print("running registerClient()")
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
        try:
            if isUsernameExists(data.get('username')):
                return HttpResponse(status=HTTPStatus.CONFLICT, content="This username is taken")
            token = insertUser(data.get('username'), data.get('password'))
            return HttpResponse(status=HTTPStatus.OK, content=token)
        except Error:
            return HttpResponse(HTTPStatus.INTERNAL_SERVER_ERROR, 'Something went  wrong, please try again later')

        return HttpResponse('Mock Token')
    return HttpResponse(status=HTTPStatus.EXPECTATION_FAILED,
                        content="Must include 'username' and 'password' in a POST request's body in a JSON format")

# def registerClient(username: str, password: str):
#     try:
#         if isUsernameExists(username):
#             return False
#         insertUser(username, password)
#     except Error as e:
#         print("Error at registerClient()")
#     except PyJWTError as e:
#         print("PyJWTError at registerClient()")


def isUsernameExists(username: str):
    print("running isUsernameExists()")
    try:
        return QuerySet(model=User).all().filter(username=username).exists()
    except Error as e:
        print("Error at isUsernameExists()")
        raise str(e)


def isUsernameAndPasswordExists(username: str, password: str):
    print("running isUsernameAndPasswordExists()")
    try:
        return QuerySet(model=User).all().filter(username=username, password=password).exists()
    except Error as e:
        print("Error at isUsernameAndPasswordExists()")
        raise str(e)


def getAllUsers():
    print("running getAllUsers()")
    try:
        return QuerySet(model=User).all().__dict__
    except Error as e:
        print("Error at getAllUsers()")
        raise str(e)


def insertUser(username: str, password: str):
    print("running insertUser()")
    token = ""
    try:
        user: User = User()
        user.username = username
        user.password = password
        token = str(encode({"usr": username, "pswd": password}, secretiveSecret, "HS256"))
        user.token = token
        user.save()
        print(f"{username}'s token is {token}")
        return token
    except Error as e:
        print("Error at insertUser()")
        raise str(e)
    except PyJWTError as e:
        print("PyJWTError at insertUser()")
        raise str(e)


def authorizeUser(jwtToken: str):
    print("running authorizeUser()")
    try:
        payload = decode(jwtToken, secretiveSecret, "HS256")
        if "usr" and "pswd" in payload.keys():
            if isUsernameAndPasswordExists(payload.get("usr"), payload.get("pswd")):
                return True
        return False
    except PyJWTError as e:
        print("PyJWTError at authorizeUser()")
        raise str(e)
