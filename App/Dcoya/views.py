from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from http import HTTPStatus
from json import loads as jsonLoads
from .models import User
from django.db.models.manager import Manager, QuerySet
from django.db.utils import Error
from jwt import encode, decode, PyJWTError
from time import time

secretiveSecret = "fpj2u6fCLsHeb6TjuvFBC9ULNmpN4xC9qW6Cz57wU969jzpEA2mPaCvb2rmwpXZXpTVWEShM4S75ysjeB3wBU3Y9QSQQu2SvwQqj5jWRMH5FWQCDCgAQuFWTdwPSKVXN"
timeToExpiration = 3600  # seconds


def registerClient(request: WSGIRequest):
    print("running registerClient()")
    if request.method == "POST":
        data: dict = jsonLoads(request.body)
        if len(data.keys()) != 2 or "username" and "password" not in data.keys():
            return HttpResponse(status=HTTPStatus.EXPECTATION_FAILED,
                                content="must include only 2 parameters: 'username' and 'password' in a JSON format")

        for k, v in data.items():
            if k == "username" or "password":
                if len(v) > 256:
                    return HttpResponse(status=HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
                                        content="each JSON parameter should not exceed 256 characters in size")
        try:
            if isUsernameExists(data.get('username')):
                return HttpResponse(status=HTTPStatus.CONFLICT, content="This username is taken")
            token = insertUser(data.get('username'), data.get('password'))
            return HttpResponse(status=HTTPStatus.OK, content=token)
        except Error:
            return HttpResponse(status=HTTPStatus.INTERNAL_SERVER_ERROR,
                                content='Something went  wrong, please try again later')
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
        raise e


def isUsernameAndPasswordExists(username: str, password: str):
    print("running isUsernameAndPasswordExists()")
    try:
        return QuerySet(model=User).all().filter(username=username, password=password).exists()
    except Error as e:
        print("Error at isUsernameAndPasswordExists()")
        raise e


def getAllUsers():
    """
    :return: a QuerySet, can be used to iterate Users inside it
    """
    print("running getAllUsers()")
    try:
        return QuerySet(model=User).all()
    except Error as e:
        print("Error at getAllUsers()")
        raise e


def insertUser(username: str, password: str):
    print("running insertUser()")
    token = ""
    expirationDate = int(time()) + timeToExpiration
    try:
        user: User = User()
        user.username = username
        user.password = password
        # TODO add expiry date

        token = str(encode({"usr": username, "pswd": password, "expDate": expirationDate}, secretiveSecret, "HS256"))
        user.token = token
        user.save()
        print(f"{username}'s token is {token}")
        return token
    except Error as e:
        print("Error at insertUser()")
        raise e
    except PyJWTError as e:
        print("PyJWTError at insertUser()")
        raise e


def authorizeUser(jwtToken: str):
    print("running authorizeUser()")
    try:
        payload = decode(jwtToken, secretiveSecret, "HS256")
        if "usr" and "pswd" and "expDate" in payload.keys():
            if payload.get("expDate") > int(time()):
                return False
            if isUsernameAndPasswordExists(payload.get("usr"), payload.get("pswd")):
                return True
        return False
    except PyJWTError as e:
        print("Invalid token at authorizeUser()")
        return False


def echo(request: WSGIRequest):
    # encodedJwt: str, msg: str
    if request.method == "POST":
        data: dict = jsonLoads(request.body)
        if len(data.keys()) != 2 or "encodedJwt" and "msg" not in data.keys():
            return HttpResponse(status=HTTPStatus.EXPECTATION_FAILED,
                                content="must include only 2 parameters: 'msg' and 'encodedJwt' in a JSON format")
        try:

            return HttpResponse(status=HTTPStatus.OK, content="")
        except Error:
            return HttpResponse(status=HTTPStatus.INTERNAL_SERVER_ERROR,
                                content='Something went  wrong, please try again later')
    pass


for user in getAllUsers():
    print(user.username)
    print(decode(user.token, secretiveSecret, "HS256"))
