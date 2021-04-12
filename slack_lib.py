import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

slack_client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

def send_slack_alert(channel, msg):
    try:
        response = slack_client.chat_postMessage(channel=channel, text=msg)
        assert response["message"]["text"] == msg
    except SlackApiError as e:
        assert e.response["ok"] is False
        assert e.response["error"]  # str like 'invalid_auth', 'channel_not_found'
        print(f"Got an error posting slack alert: {e.response['error']}")