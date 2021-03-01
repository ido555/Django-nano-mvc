import json
import requests
from requests import Response
from Client.enums import ApiURIs


def newUserJSON():
    user = input("Username: ")
    password = input("Password: ")
    return json.dumps({"username": user, "password": password})


def apiPOST(endpoint: ApiURIs, tempJson):
    req: Response = requests.post(endpoint.value, data=tempJson)
    return req


# r.status_code
# r.json()
# a = newUserJSON()
# print(a)
JWT = ""
while True:
    if JWT == "":
        print("Register a new user: \n")
        j = newUserJSON()
        r: Response = apiPOST(ApiURIs.Register, j)
        print(r.status_code)
        print(r.content)
        continue

    print("1 - echo \n2 - time")
    sel = str(input("enter selection"))
    if JWT != "":
        if sel == "1":
            r: Response = apiPOST(ApiURIs.Echo.value, json.dumps({"encodedJwt": JWT, "msg": input("enter text")}))
            print(r.status_code)
            print(str(r.content))
        if sel == "2":
            r: Response = apiPOST(ApiURIs.Time.value, json.dumps({"encodedJwt": JWT}))
            print(f"status code: {r.status_code}")
            print(str(r.content))
