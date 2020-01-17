from flask import Flask, request, make_response, Response
import os
import slack

app = Flask(__name__)


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

@app.route('/hello', methods=['POST'])
def hello():
    return 'Hello Slack! ' + request.form['text']


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
