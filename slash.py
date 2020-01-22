from flask import Flask, request, make_response, Response
import os
import slack
import os
import logging
import ssl as ssl_lib
import certifi
import json
from onboarding_tutorial import OnboardingTutorial

app = Flask(__name__)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())
ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
slack_token = os.environ["SLACK_BOT_TOKEN"]
rtm_client = slack.RTMClient(token=slack_token, ssl=ssl_context)
    # return request.form[team_id]
    # return 'Rate your experience. 1 meaning the '

# @app.route('/feedback', methods= ['POST'])
# def
# class OnboardingTutorial:
#     """Constructs the onboarding message and stores the state of which tasks were completed."""
#
#     WELCOME_BLOCK = {
#         "type": "section",
#         "text": {
#             "type": "mrkdwn",
#             "text": (
#                 "Welcome to Slack! :wave: We're so glad you're here. :blush:\n\n"
#                 "*Get started by completing the steps below:*"
#             ),
#         },
#     }
#     DIVIDER_BLOCK = {"type": "divider"}
#
#     def __init__(self, channel):
#         self.channel = channel
#         self.username = "pythonboardingbot"
#         self.icon_emoji = ":robot_face:"
#         self.timestamp = ""
#         self.reaction_task_completed = False
#         self.pin_task_completed = False
#
#     def get_message_payload(self):
#         return {
#             "ts": self.timestamp,
#             "channel": self.channel,
#             "username": self.username,
#             "icon_emoji": self.icon_emoji,
#             "blocks": [
#                 self.WELCOME_BLOCK,
#                 self.DIVIDER_BLOCK,
#                 *self._get_reaction_block(),
#                 self.DIVIDER_BLOCK,
#                 *self._get_pin_block(),
#             ],
#         }
#
#     def _get_reaction_block(self):
#         task_checkmark = self._get_checkmark(self.reaction_task_completed)
#         text = (
#             f"{task_checkmark} *Add an emoji reaction to this message* :thinking_face:\n"
#             "You can quickly respond to any message on Slack with an emoji reaction."
#             "Reactions can be used for any purpose: voting, checking off to-do items, showing excitement."
#         )
#         information = (
#             ":information_source: *<https://get.slack.help/hc/en-us/articles/206870317-Emoji-reactions|"
#             "Learn How to Use Emoji Reactions>*"
#         )
#         return self._get_task_block(text, information)
#
#     def _get_pin_block(self):
#         task_checkmark = self._get_checkmark(self.pin_task_completed)
#         text = (
#             f"{task_checkmark} *Pin this message* :round_pushpin:\n"
#             "Important messages and files can be pinned to the details pane in any channel or"
#             " direct message, including group messages, for easy reference."
#         )
#         information = (
#             ":information_source: *<https://get.slack.help/hc/en-us/articles/205239997-Pinning-messages-and-files"
#             "|Learn How to Pin a Message>*"
#         )
#         return self._get_task_block(text, information)
#
#     @staticmethod
#     def _get_checkmark(task_completed: bool) -> str:
#         if task_completed:
#             return ":white_check_mark:"
#         return ":white_large_square:"
#
#     @staticmethod
#     def _get_task_block(text, information):
#         return [
#             {"type": "section", "text": {"type": "mrkdwn", "text": text}},
#             {"type": "context", "elements": [{"type": "mrkdwn", "text": information}]},
#         ]

@app.route('/', methods=['GET','POST'])
# def hello():
#     a= request.get('http://3206b703.ngrok.io')
#     print(a.content)
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
    return thing()

    # data = payload["data"]
    # web_client = payload["web_client"]
    # channel_id = payload["item"]["channel"]
    # user_id = payload["user"]
    # val = request.form['payload']#["actions"]["value"]
    # print(message["user"])
    # if actions.action_id == "improv":
    #     print("hi")

def button_clicked():
    x = requests.get('https://hooks.slack.com/services/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')
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
    if text and text.lower() == "feedback":
        return start_onboarding(web_client, user_id, channel_id)



if __name__ == '__main__':
    port = int(os.environ.get('PORT', 443))
    app.run(host='0.0.0.0', port=port, debug=True)
