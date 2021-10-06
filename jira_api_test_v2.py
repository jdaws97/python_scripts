import requests
import json
import os
import csv
from requests.auth import HTTPBasicAuth
import pwd
import argparse


project_type = "JT"



headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

osuser = pwd.getpwuid(os.getuid()).pw_name


def grab_issues(auth: str, username: str, email: str, start: int):

    url = f"https://{username}.atlassian.net/rest/api/2/search"

    response = requests.request(
        "GET",
        url,
        headers=headers,
        auth=auth
    )

    if response.status_code != 200:
        raise Exception("You don't have permission or it doesn't exist")


    data = json.loads(response.text)
    total = data["total"]
    maxResults = data["maxResults"]
    start = start + maxResults

    if start < total:
        grab_issues(auth, username, email, int(start))


    tickets = []
    tickets.extend(data["issues"])

    count = 0

    with open(f'/home/{osuser}{os.sep}JT_SoftwareRequest.csv', 'w') as file:

        for issue in tickets:

            if count == 0:

                file.write("Key,Summary,Status\n")
                count += 1

            file.write(f"{issue['key']},{issue['fields']['summary']},{issue['fields']['status']['name']} \n")


def main():

    parser = argparse.parser = argparse.ArgumentParser(
        description = "Input the following data to receive a query!"
    )

    parser.add_argument("-e", "--atlassian_email",
            required=True,
            help="Atlassian emailneeded for auth request"
    )

    parser.add_argument("-u", "--atlassian_username",
            required=True,
            help="Atlassian username needed for jira url"
    )

    parser.add_argument("-k", "--api_key",
            required=True,
            help="Generate an API Key from your account and paste it here, it's used for authentication"
)

    args = parser.parse_args()

    if not args.atlassian_email and not args.api_key and not args.atlassian_username:
        parser.error("No username or key")

    auth = HTTPBasicAuth("jarod.daws@gmail.com", f"{args.api_key}")




    grab_issues(auth, args.atlassian_username, args.atlassian_email, 0)


if __name__ =="__main__":
    main()