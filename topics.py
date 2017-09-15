"""Gets json from Zendesk"""

import base64
import httplib2
import json
import datetime


URL_BASE = "https://saucelabs.zendesk.com/api/v2/"


def get_topics_json():
    "Obtain topics with username and password"

    url = URL_BASE + "help_center/community/topics.json"
    # log_name = "log_{}.log".format(job_id)
    http_conn = httplib2.Http()
    # http_conn.add_credentials(admin, access_key)
    # user_pass = base64.b64encode("{}:{}".format(username, password))
    # headers = {'Authorization' : 'Basic {}'.format(user_pass)}
    _, response = http_conn.request(url, method="GET")

    load = json.loads(response) 

    return load['topics'] #TODO: Test that checks "topics" is valid

def check_last_update_date(topics):

    for topic in topics:
        last_update = topic['updated_at']
        print last_update
        datetime_last_update = datetime.datetime.strptime(last_update,'%Y-%m-%dT%H:%M:%SZ')
        datetime_now = datetime.datetime.now()

        print datetime_now - datetime_now

def get_agents_ids(username, password):

    url = URL_BASE + "users.json"
        # log_name = "log_{}.log".format(job_id)
    print url
    http_conn = httplib2.Http()

    # http_conn.add_credentials(admin, access_key)
    user_pass = base64.b64encode("{}:{}".format(username, password))
    headers = {'Authorization' : 'Basic {}'.format(user_pass)}
    _, response = http_conn.request(url, method="GET", headers=headers)

    load = json.loads(response)

    return load

def send_request(endpoint, method, username, password):

    headers = None
    url = URL_BASE + endpoint

    http_conn = httplib2.Http()


    if username is not None and password is not None:

        user_pass = base64.b64encode("{}:{}".format(username, password))
        headers = {'Authorization' : 'Basic {}'.format(user_pass)}

    _, response = http_conn.request(url, method=method, headers=headers)

    return response

def main():
    username = ""
    password = ""
    topics = get_topics_json()
    check_last_update_date(topics)
    agents = get_agents_ids(username, password)
    print agents

if __name__ == '__main__':
    main()