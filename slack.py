import httplib2
import os
import logging
import json

logger = logging.getLogger(__name__)

message = {
    "text": "New community update!",
    "attachments": [
        {
			"author_name":"Bobby Tables",
			"title_link":"https://support.saucelabs.com",
			"title" : "TOPIC TITLE"
        }
    ]
}

SLACK_WEBHOOK = os.environ.get('SLACK_WEBHOOK')

def send_request():

    headers = {'Content-type' : 'application/json'}
    url = SLACK_WEBHOOK

    logger.debug("Sending request to: %s", url)

    http_conn = httplib2.Http()
    payload = json.dumps(message)

    status, response = http_conn.request(url, method="POST", headers=headers,body=payload) #TODO: Check status code and throw error
    logger.debug("Status: %s",status)

    return response

if __name__ == '__main__':
    send_request()

