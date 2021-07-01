from enum import Enum


class ApiURIs(Enum):
    BaseURL = "http://127.0.0.1:8000"
    Register = BaseURL + "/register"
    Echo = BaseURL + "/echo"
    Time = BaseURL + "/time"
