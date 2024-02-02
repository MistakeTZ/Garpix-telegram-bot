import os
import requests
from requests.auth import HTTPBasicAuth


"""
def test():
    password = "c;mMx.0h"

    url = "https://api.getpostman.com/me"
    auth = HTTPBasicAuth('olebedev', password)
    headers = {
        'X-API-Key': password
    }

    r = requests.get(url, auth=auth)
    print(r)
    print(r.json)
"""


async def check_promo(username, email, firstname, lastname, token, groupid, courseid) -> bool:
    return True
    url = "http://study.infra.garpix.com/api/v1/change_users/create_user/"
    headers = {
        "username": username,
        "email": email,
        "firstname": firstname,
        "lastname": lastname,
        "domain": "study.garpix.com",
        "token_bot": os.getenv("TOKEN_BOT"),
        "token": os.getenv("TOKEN"),
        "callback": os.getenv("CALLBACK"),
        "groupid": groupid,
        "courseid": courseid
    }
    r = requests.get(url, headers=headers)
    return r.json()