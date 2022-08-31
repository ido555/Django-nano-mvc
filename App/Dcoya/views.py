from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from http import HTTPStatus
from json import loads as jsonLoads
from json import JSONDecodeError
from .models import User
from django.db.models.manager import Manager, QuerySet
from django.db.utils import Error
from jwt import encode, decode, PyJWTError
from time import time as serverTimestamp
from .exceptions import ExpiredJWT, JWTLength

secretiveSecret = "fpj2u6fCLsHeb6TjuvFBC9ULNmpN4xC9qW6Cz57wU969jzpEA2mPaCvb2rmwpXZXpTVWEShM4S75ysjeB3wBU3Y9QSQQu2SvwQqj5jWRMH5FWQCDCgAQuFWTdwPSKVXN"
timeToExpiration = 3600  # seconds
JWTMaxLength = 1024
MSGMaxLength = 4096


def registerClient(request: WSGIRequest):
    print("running registerClient()")
    if request.method == "POST":
        try:
            data: dict = jsonLoads(request.body)
        except JSONDecodeError:
            return HttpResponse(status=HTTPStatus.EXPECTATION_FAILED,
                                content="Invalid JSON")
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
    expirationDate = int(serverTimestamp()) + timeToExpiration
    try:
        user: User = User()
        user.username = username
        user.password = password
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
        if len(jwtToken) > JWTMaxLength:
            raise JWTLength
        payload = decode(jwtToken, secretiveSecret, "HS256")
        if "usr" and "pswd" and "expDate" in payload.keys():
            if payload.get("expDate") < int(serverTimestamp()):
                raise ExpiredJWT
            if isUsernameAndPasswordExists(payload.get("usr"), payload.get("pswd")):
                return True
        return False
    except PyJWTError as e:
        print("Invalid token at authorizeUser()")
        return False


def echo(request: WSGIRequest):
    if request.method == "POST":
        try:
            data: dict = jsonLoads(request.body)
        except JSONDecodeError:
            return HttpResponse(status=HTTPStatus.EXPECTATION_FAILED,
                                content="Invalid JSON")
        if len(data.keys()) != 2 or "encodedJwt" and "msg" not in data.keys():
            return HttpResponse(status=HTTPStatus.EXPECTATION_FAILED,
                                content="must include only 2 parameters: 'msg' and 'encodedJwt' in a JSON format")
        encodedJwt = data.get("encodedJwt")
        msg = data.get("msg")
        if len(msg) > MSGMaxLength:
            return HttpResponse(status=HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
                                content=f"'msg' parameter cannot exceed {MSGMaxLength} characters")
        try:
            if authorizeUser(encodedJwt):
                return HttpResponse(status=HTTPStatus.OK, content=msg)
            else:
                return HttpResponse(status=HTTPStatus.UNAUTHORIZED, content="JWT invalid")
        except ExpiredJWT:
            print("ExpiredJWT in echo()")
            return HttpResponse(status=HTTPStatus.EXPECTATION_FAILED,
                                content='Provided JWT is expired')
        except JWTLength:
            print("JWTLength error at echo()")
            return HttpResponse(status=HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
                                content=f"'encodedJwt' parameter cannot exceed {JWTMaxLength} characters")
        except Error:
            print("error at echo()")
            return HttpResponse(status=HTTPStatus.INTERNAL_SERVER_ERROR,
                                content='Something went  wrong, please try again later')
    return HttpResponse(status=HTTPStatus.EXPECTATION_FAILED,
                        content="Must include 'encodedJwt' and 'msg' in a POST request's body in a JSON format")


def time(request: WSGIRequest):
    if request.method == "POST":
        try:
            data: dict = jsonLoads(request.body)
        except JSONDecodeError:
            return HttpResponse(status=HTTPStatus.EXPECTATION_FAILED,
                                content="Invalid JSON")
        if len(data.keys()) != 1 or "encodedJwt" not in data.keys():
            return HttpResponse(status=HTTPStatus.EXPECTATION_FAILED,
                                content="must include only 1 parameter: 'encodedJwt' in a JSON format")
        encodedJwt = data.get("encodedJwt")
        if len(encodedJwt) > JWTMaxLength:
            return HttpResponse(status=HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
                                content=f"'encodedJwt' parameter cannot exceed {JWTMaxLength} characters")
        try:
            if authorizeUser(encodedJwt):
                return HttpResponse(status=HTTPStatus.OK, content=int(serverTimestamp()))
            else:
                return HttpResponse(status=HTTPStatus.UNAUTHORIZED, content="JWT invalid")
        except ExpiredJWT:
            print("expired JWT in echo()")
            return HttpResponse(status=HTTPStatus.EXPECTATION_FAILED,
                                content='Provided JWT is expired')
        except JWTLength:
            print("JWTLength error at echo()")
            return HttpResponse(status=HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
                                content=f"'encodedJwt' parameter cannot exceed {JWTMaxLength} characters")
        except Error:
            print("error at echo()")
            return HttpResponse(status=HTTPStatus.INTERNAL_SERVER_ERROR,
                                content='Something went  wrong, please try again later')
    return HttpResponse(status=HTTPStatus.EXPECTATION_FAILED,
                        content="Must include 'encodedJwt' in a POST request's body in a JSON format")

