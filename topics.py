"""Gets json from Zendesk"""

import base64
import httplib2
import json
import datetime
import os


URL_BASE = "https://saucelabs.zendesk.com/api/v2/"


def get_topics_json():
    "Obtain topics with username and password"

    endpoint =  "help_center/community/topics.json"

    response = send_request(endpoint, "GET")

    load = json.loads(response) 

    return load['topics'] #TODO: Test that checks "topics" is valid

def check_last_update_date(topics):

    for topic in topics:
        last_update = topic['updated_at']
        print last_update
        datetime_last_update = datetime.datetime.strptime(last_update,'%Y-%m-%dT%H:%M:%SZ')
        datetime_now = datetime.datetime.now()

        print datetime_now - datetime_last_update

def get_agents_ids(username, password):

    endpoint = "users.json"
    response = send_request(endpoint, "GET", username, password)

    load = json.loads(response)

    return load

def send_request(endpoint, method, username=None, password=None):

    headers = None
    url = URL_BASE + endpoint

    http_conn = httplib2.Http()


    if username is not None and password is not None:

        user_pass = base64.b64encode("{}:{}".format(username, password))
        headers = {'Authorization' : 'Basic {}'.format(user_pass)}

    _, response = http_conn.request(url, method=method, headers=headers)

    return response

def main():
    username = os.environ.get('ZENDESK_USERNAME')
    password = os.environ.get('ZENDESK_PASSWORD')
    topics = get_topics_json()
    check_last_update_date(topics)
    agents = get_agents_ids(username, password)
    print agents

if __name__ == '__main__':
    main()