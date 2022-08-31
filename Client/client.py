import json
import requests
from requests import Response
from enums import ApiURIs


def newUserJSON():
    user = input("Username: ")
    password = input("Password: ")
    return json.dumps({"username": user, "password": password})


def apiPOST(endpoint: ApiURIs, tempJson):
    res: Response = requests.post(endpoint.value, data=tempJson)
    return res


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
        if r.status_code != 200:
            print(f"status code: {r.status_code}")
            print(str(r.text))
        else:
            JWT = r.text
        continue

    print("1 - echo \n2 - time \n3 - quit")
    sel = str(input("enter selection: "))
    if JWT != "":
        if sel == "1":
            r: Response = apiPOST(ApiURIs.Echo, json.dumps({"encodedJwt": JWT, "msg": input("enter text: ")}))
            if r.status_code != 200:
                print(f"status code: {r.status_code}")
                print(str(r.text))
            else:
                print(f"echo: {r.text}")
        if sel == "2":
            r: Response = apiPOST(ApiURIs.Time, json.dumps({"encodedJwt": JWT}))

            if r.status_code != 200:
                print(f"status code: {r.status_code}")
                print(str(r.text))
            else:
                print(f"server timestamp: {r.text}")
        if sel == "3":
            break
