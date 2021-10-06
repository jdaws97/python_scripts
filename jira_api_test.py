import requests 
import json
from requests.auth import HTTPBasicAuth
import pwd
import os


url = "https://jaroddaws.atlassian.net/rest/api/2/issue/"

auth = HTTPBasicAuth("jarod.daws@gmail.com", "oy4LyztoxFdZbbAgvY1CF70C")


headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

payload = json.dumps(
    {
    "update": {},
    "fields": {
        "project": {
            "id": "10001"
        },
        "summary": "Create an issue with a python script",
        "issuetype": {
            "name": "Task"
        },
        
        "description": "Lorem ipsum.......................",

        }
    }
)

response = requests.request(
    "POST",
    url,
    data=payload,
    headers=headers,
    auth=auth
)






print(response)

