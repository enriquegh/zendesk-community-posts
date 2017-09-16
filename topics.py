"""Gets json from Zendesk"""

import base64
import httplib2
import json
import datetime
import os
import logging

URL_BASE = "https://saucelabs.zendesk.com/api/v2/"
username = os.environ.get('ZENDESK_USERNAME')
password = os.environ.get('ZENDESK_PASSWORD')

logger = logging.getLogger(__name__)


def get_recent_posts_json():
    "Obtain recent posts sorted by recent activity"

    endpoint =  "help_center/community/posts.json?sort_by=recent_activity"

    logger.info("Sending %s request to Zendesk",endpoint)
    response = send_request(endpoint, "GET")

    load = json.loads(response) 

    return load['posts'] #TODO: Test that checks "posts" is valid

def check_last_update_date(posts):

    recent_posts = []

    for post in posts:
        last_update = post['updated_at']
        datetime_last_update = datetime.datetime.strptime(last_update,'%Y-%m-%dT%H:%M:%SZ')
        datetime_now = datetime.datetime.now()

        time_difference =  datetime_now - datetime_last_update

        if time_difference.days < 8 and post['status'] is "none":
            recent_posts.append(post)
            # print time_difference.days
            # post_id = post['id']
            # print post_id
            # print check_last_commenter(post_id)
    return recent_posts

def check_last_commenter(id):

    endpoint = "community/posts/{post_id}/comments.json".format(post_id=id)

    response = send_request(endpoint, "GET", username, password)

    load = json.loads(response)

    return load['comments'][0]

def is_comment_by_agent(agent_ids, comment):

    author_id = comment['author_id']
    if author_id not in agent_ids:
        logger.info("Post needs answering: %s", comment['html_url'])


def get_agents_ids():

    endpoint = "users.json?role=agent"

    logger.info("Sending %s request to Zendesk",endpoint)
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
    logger.debug("Sending request to: %s", url)

    http_conn = httplib2.Http()


    if username is not None and password is not None:

        user_pass = base64.b64encode("{}:{}".format(username, password))
        headers = {'Authorization' : 'Basic {}'.format(user_pass)}

    status, response = http_conn.request(url, method=method, headers=headers)
    logger.debug("Status: %s",status)

    return response

def main():

    logger.info("Getting recent posts")
    posts = get_recent_posts_json()
    logger.info("Checking recently upated posts")

    recent_posts = check_last_update_date(posts)
    logger.info("Getting agent ID's")
    agent_ids = get_agents_ids()
    logger.debug("Agent ID's: %s", agent_ids)

    if recent_posts:
        for post in recent_posts:
            comment = check_last_commenter(post['id'])
            is_comment_by_agent(agent_ids, comment)

if __name__ == '__main__':
    main()