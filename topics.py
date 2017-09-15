"""Gets json from Zendesk"""

import base64
import httplib2
import json
import datetime
import os


URL_BASE = "https://saucelabs.zendesk.com/api/v2/"
username = os.environ.get('ZENDESK_USERNAME')
password = os.environ.get('ZENDESK_PASSWORD')


def get_recent_posts_json():
    "Obtain recent posts sorted by recent activity"

    endpoint =  "help_center/community/posts.json?sort_by=recent_activity"

    response = send_request(endpoint, "GET")

    load = json.loads(response) 

    return load['posts'] #TODO: Test that checks "posts" is valid

def check_last_update_date(posts):

    for post in posts:
        last_update = post['updated_at']
        datetime_last_update = datetime.datetime.strptime(last_update,'%Y-%m-%dT%H:%M:%SZ')
        datetime_now = datetime.datetime.now()

        time_difference =  datetime_now - datetime_last_update

        if time_difference.days < 8:

            print time_difference.days
            post_id = post['id']
            print post_id
            print check_last_commenter(post_id)

def check_last_commenter(id):

    endpoint = "community/posts/{post_id}/comments.json".format(post_id=id)

    response = send_request(endpoint, "GET", username, password)

    load = json.loads(response)

    return load['comments'][0]


def get_agents_ids():

    endpoint = "users.json?role=agent"
    response = send_request(endpoint, "GET", username, password)

    load = json.loads(response)

    agent_ids = []

    for user in load['users']: #TODO: Test that checks "users" is valid
        user_id = user['id']
        agent_ids.append(user_id)
    return agent_ids

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
    posts = get_recent_posts_json()
    check_last_update_date(posts)
    # agents = get_agents_ids()
    # print agents

if __name__ == '__main__':
    main()