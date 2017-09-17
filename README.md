# zendesk-community-posts

This script will send a message to Slack whenever there's a new Community post or comment on a post that is not by an Agent.

Has three environment variables:

$ZENDESK_USERNAME - Username/email of Agent or Admin in order to retrieve Agent IDs

$ZENDESK_PASSWORD - Password of Agent or Admin in order to retrieve Agent IDs

$SLACK_WEBHOOK - Webhook where message will be sent

Once environment variables are set run:

`python run.py`
