import os
import logging
import slack
import ssl as ssl_lib
import certifi
import json
import requests
from onboarding_tutorial import OnboardingTutorial
# from flask import Flask, request, make_response, Response
#
# app = Flask(__name__)
# For simplicity we'll store our app data in-memory with the following data structure.
# onboarding_tutorials_sent = {"channel": {"user_id": OnboardingTutorial}}
# num_help = 0

onboarding_tutorials_sent = {}
feeling = 0


# def thing():
#     webhook_url= "https://hooks.slack.com/services/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"
#     t = {"text": "Hello, world."}
#     # JSON.stringify(t)
#     response = requests.post(
#     webhook_url, data=json.dumps(t),
#     headers={'Content-Type': 'application/json'}
#     )
#     a = requests.get('http://3206b703.ngrok.io')
#     print(a.text)
def helper(text):
    t = {"text": text}
    webhook_url= "https://hooks.slack.com/services/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"

    # JSON.stringify(t)
    response = requests.post(
    webhook_url, data=json.dumps(t),
    headers={'Content-Type': 'application/json'}
    )

def start_onboarding(web_client: slack.WebClient, user_id: str, channel: str):
    # Create a new onboarding tutorial.
    onboarding_tutorial = OnboardingTutorial(channel)

    # Get the onboarding message payload
    message = onboarding_tutorial.get_message_payload()

    # Post the onboarding message in Slack
    response = web_client.chat_postMessage(**message)

    # Capture the timestamp of the message we've just posted so
    # we can use it to update the message after a user
    # has completed an onboarding task.
    onboarding_tutorial.timestamp = response["ts"]

    # Store the message sent in onboarding_tutorials_sent
    if channel not in onboarding_tutorials_sent:
        onboarding_tutorials_sent[channel] = {}
    onboarding_tutorials_sent[channel][user_id] = onboarding_tutorial

    message = onboarding_tutorial.get_message_payload()
    # return thing()

    # data = payload["data"]
    # web_client = payload["web_client"]
    # channel_id = payload["item"]["channel"]
    # user_id = payload["user"]
    # val = request.form['payload']#["actions"]["value"]
    # print(message["user"])
    # if actions.action_id == "improv":
    #     print("hi")

# def button_clicked():
#     x = requests.get('https://hooks.slack.com/services/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')
    # print(x.content)


# ================ Team Join Event =============== #
# When the user first joins a team, the type of the event will be 'team_join'.
# Here we'll link the onboarding_message callback to the 'team_join' event.

@slack.RTMClient.run_on(event="team_join")
def onboarding_message(**payload):
    """Create and send an onboarding welcome message to new users. Save the
    time stamp of this message so we can update this message in the future.
    """
    # Get WebClient so you can communicate back to Slack.
    web_client = payload["web_client"]

    # Get the id of the Slack user associated with the incoming event
    user_id = payload["data"]["user"]["id"]

    # Open a DM with the new user.
    response = web_client.im_open(user_id)
    channel = response["channel"]["id"]

    # use = {"user_id":user_id}
    # x = request.post(url,JSON.stringify(use))
    # print(x.text)
    # Post the onboarding message.
    start_onboarding(web_client, user_id, channel)


# ============= Reaction Added Events ============= #
# When a users adds an emoji reaction to the onboarding message,
# the type of the event will be 'reaction_added'.
# Here we'll link the update_emoji callback to the 'reaction_added' event.
@slack.RTMClient.run_on(event="reaction_added")
def update_emoji(**payload):
    """Update the onboarding welcome message after receiving a "reaction_added"
    event from Slack. Update timestamp for welcome message as well.
    """
    data = payload["data"]
    web_client = payload["web_client"]
    channel_id = data["item"]["channel"]
    user_id = data["user"]

    if channel_id not in onboarding_tutorials_sent:
        return

    # Get the original tutorial sent.
    onboarding_tutorial = onboarding_tutorials_sent[channel_id][user_id]

    # Mark the reaction task as completed.
    onboarding_tutorial.reaction_task_completed = True

    # Get the new message payload
    message = onboarding_tutorial.get_message_payload()

    # Post the updated message in Slack
    updated_message = web_client.chat_update(**message)

    # Update the timestamp saved on the onboarding tutorial object
    onboarding_tutorial.timestamp = updated_message["ts"]

# =============== Pin Added Events ================ #
# When a users pins a message the type of the event will be 'pin_added'.
# Here we'll link the update_pin callback to the 'reaction_added' event.
@slack.RTMClient.run_on(event="pin_added")
def update_pin(**payload):
    """Update the onboarding welcome message after receiving a "pin_added"
    event from Slack. Update timestamp for welcome message as well.
    """
    data = payload["data"]
    web_client = payload["web_client"]
    channel_id = data["channel_id"]
    user_id = data["user"]
    # val = data["action"]["value"]
    print(payload)

    # Get the original tutorial sent.
    onboarding_tutorial = onboarding_tutorials_sent[channel_id][user_id]

    # Mark the pin task as completed.
    onboarding_tutorial.pin_task_completed = True

    # Get the new message payload
    message = onboarding_tutorial.get_message_payload()

    # Post the updated message in Slack
    updated_message = web_client.chat_update(**message)

    # Update the timestamp saved on the onboarding tutorial object
    onboarding_tutorial.timestamp = updated_message["ts"]



# ============== Message Events ============= #
# When a user sends a DM, the event type will be 'message'.
# Here we'll link the message callback to the 'message' event.


@slack.RTMClient.run_on(event="message")


def message(**payload):
    """Display the onboarding welcome message after receiving a message
    that contains "feedback".
    """
    data = payload["data"]
    web_client = payload["web_client"]
    channel_id = data.get("channel")
    user_id = data.get("user")
    text = data.get("text")

    # if text and text.lower() == "start":
    #     return start_onboarding(web_client, user_id, channel_id)
    # print(num_help)
    if text and text.lower() == "feedback":
        print("whyycgecy")
        global num_help
        num_help = 0
        return start_onboarding(web_client, user_id, channel_id)
    elif text and text.lower() == "1":
        # data = payload["data"]
        # web_client = payload["web_client"]
        # channel_id = data["channel_id"]
        # user_id = data["user"]
        # text= ""
        print("++++++++++++++++")
        print(num_help)
        print("+++++++++++++++")
        onboarding_tutorial = onboarding_tutorials_sent[channel_id][user_id]

        me = onboarding_tutorial.get_mess_sad()

        # Post the updated message in Slack
        updated_message = web_client.chat_postMessage(**me)

        # Update the timestamp saved on the onboarding tutorial object
        onboarding_tutorial.timestamp = updated_message["ts"]
        num_help = 1
        print("huef")
        return
    elif text and text.lower() == "5":
        # data = payload["data"]
        # web_client = payload["web_client"]
        # channel_id = data["channel_id"]
        # user_id = data["user"]
        # text= ""
        onboarding_tutorial = onboarding_tutorials_sent[channel_id][user_id]
        print("=====================")
        print(onboarding_tutorials_sent)
        print("=====================")

        me = onboarding_tutorial.get_mess_happy()

        # Post the updated message in Slack
        updated_message = web_client.chat_postMessage(**me)

        # Update the timestamp saved on the onboarding tutorial object
        onboarding_tutorial.timestamp = updated_message["ts"]
        num_help=1
        print("bru")
        return
    elif text!= "1" or text != "5":
        # print(num_help)
        # print(web_client.conversations_history(channel=channel_id, limit=2))
        print("++++++++++++++++")
        print(num_help)
        print(user_id)
        print("+++++++++++++++")
        if num_help == 1 and user_id != None:
            print(text)
            helper(text)
            # t = {"text": text}
            # webhook_url= "https://hooks.slack.com/services/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"
            #
            # # JSON.stringify(t)
            # response = requests.post(
            # webhook_url, data=json.dumps(t),
            # headers={'Content-Type': 'application/json'}
            # )


    # #     data = payload["data"]
    # #     web_client = payload["web_client"]
    # #     channel_id = data.get("channel")
    # #     user_id = data.get("user")
    # #     text = data.get("text")
    #     print("=====================")
    #     print(onboarding_tutorials_sent)
    #     # print(onboarding_tutorials_sent[channel_id])
    #     # onboarding_tutorial = OnboardingTutorial(channel_id)
    #     # onboarding_tutorial = onboarding_tutorials_sent[channel_id][user_id]
    # #
    #     me = onboarding_tutorial.get_mess_sad()
    # #
    # #     # Post the updated message in Slack
    #     updated_message = web_client.chat_update(**me)
    #     onboarding_tutorial.timestamp = updated_message["ts"]



        # return hi(**payload);
# def hi(**payload):
#     feeling = 1
#     data = payload["data"]
#     web_client = payload["web_client"]
#     channel_id = data["channel_id"]
#     user_id = data["user"]
#     m = "why u feel like this man"
    # web_client.chat_postMessage(m)

if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
    slack_token = os.environ["SLACK_BOT_TOKEN"]
    rtm_client = slack.RTMClient(token=slack_token, ssl=ssl_context)
    # port = int(os.environ.get('PORT', 80))
    # app.run(host='0.0.0.0', port=port, debug=True)
    rtm_client.start()
