class OnboardingTutorial:
    """Constructs the onboarding message and stores the state of which tasks were completed."""

    WELCOME_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                "Welcome to the feedback central! :wave: You can address any concerns you have here.\n\n"
                "*Get started by rating how you feel, 1 being needs improvement and 5 being satisfied:*"
            ),
        },
    }
    DIVIDER_BLOCK = {"type": "divider"}
    SAD_BLOCK= {
    "type":"section",
    "text":{
        "type": "mrkdwn",
        "text": (
            "Sorry to hear :cry: Please let us know *what* and *why* you were dissapointed. \n"
            "Also please detail how you think we can *improve* and any details you feel necessary\n"
        ),
    },
    }
    HAPPY_BLOCK= {
    "type":"section",
    "text":{
        "type": "mrkdwn",
        "text": (
            "Great! :smiley: Let us know *what* and *why* you enjoyed. \n "
            "Also please detail how you think we can *improve* and any details you feel necessary\n"
        ),
    },
    }
    OTHER_BLOCK= {
    "type":"section",
    "text":{
        "type": "mrkdwn",
        "text": (
            "Thank you for your feedback"
        ),
    },
    }
    INCORRECT_BLOCK= {
    "type":"section",
    "text":{
        "type": "mrkdwn",
        "text": (
            "Invalid input, please type 1 or 5"
        ),
    },
    }
    BAD_BLOCK= {
    "type":"section",
    "text":{
        "type": "mrkdwn",
        "text": (
            "Inappropriate language is not allowed, type either 1 or 5 again if you would like to post feedback"
        ),
    },
    }

# }

    def __init__(self, channel):
        self.channel = channel
        self.username = "feedback_bot"
        self.icon_emoji = ":robot_face:"
        self.timestamp = ""
        self.reaction_task_completed = False
        self.pin_task_completed = False

    def get_message_payload(self):
        return {
            "ts": self.timestamp,
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "blocks": [
                self.WELCOME_BLOCK,
                self.DIVIDER_BLOCK,
                # self.Y_N,
                # *self._get_reaction_block(),
                # self.DIVIDER_BLOCK,
                # *self._get_pin_block(),
            ],

        }
    def get_mess_inap(self):
        return{
            "ts": self.timestamp,
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "blocks": [
                # self.WELCOME_BLOCK,
                self.BAD_BLOCK,
                self.DIVIDER_BLOCK,
                # self.Y_N,
                # *self._get_reaction_block(),
                # self.DIVIDER_BLOCK,
                # *self._get_pin_block(),
            ],

        }
    def get_mess_incor(self):
        return{
            "ts": self.timestamp,
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "blocks": [
                # self.WELCOME_BLOCK,
                self.INCORRECT_BLOCK,
                self.DIVIDER_BLOCK,
                # self.Y_N,
                # *self._get_reaction_block(),
                # self.DIVIDER_BLOCK,
                # *self._get_pin_block(),
            ],

        }
    def get_mess_sad(self):
        return{
            "ts": self.timestamp,
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "blocks": [
                # self.WELCOME_BLOCK,
                self.SAD_BLOCK,
                self.DIVIDER_BLOCK,
                # self.Y_N,
                # *self._get_reaction_block(),
                # self.DIVIDER_BLOCK,
                # *self._get_pin_block(),
            ],

        }
    def get_mess_happy(self):
        return{
            "ts": self.timestamp,
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "blocks": [
                # self.WELCOME_BLOCK,
                self.HAPPY_BLOCK,
                self.DIVIDER_BLOCK,
                # self.Y_N,
                # *self._get_reaction_block(),
                # self.DIVIDER_BLOCK,
                # *self._get_pin_block(),
            ],

        }
    def get_mess_other(self):
        return{
            "ts": self.timestamp,
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "blocks": [
                # self.WELCOME_BLOCK,
                self.OTHER_BLOCK,
                self.DIVIDER_BLOCK,
                # self.Y_N,
                # *self._get_reaction_block(),
                # self.DIVIDER_BLOCK,
                # *self._get_pin_block(),
            ],

        }

    def _get_reaction_block(self):
        task_checkmark = self._get_checkmark(self.reaction_task_completed)
        text = (
            f"{task_checkmark} *Add an emoji reaction to this message* :thinking_face:\n"
            "You can quickly respond to any message on Slack with an emoji reaction."
            "Reactions can be used for any purpose: voting, checking off to-do items, showing excitement."
        )
        information = (
            ":information_source: *<https://get.slack.help/hc/en-us/articles/206870317-Emoji-reactions|"
            "Learn How to Use Emoji Reactions>*"
        )
        return self._get_task_block(text, information)

    def _get_pin_block(self):
        task_checkmark = self._get_checkmark(self.pin_task_completed)
        text = (
            f"{task_checkmark} *Pin this message* :round_pushpin:\n"
            "Important messages and files can be pinned to the details pane in any channel or"
            " direct message, including group messages, for easy reference."
        )
        information = (
            ":information_source: *<https://get.slack.help/hc/en-us/articles/205239997-Pinning-messages-and-files"
            "|Learn How to Pin a Message>*"
        )
        # information = ()
        sec_info= ()
        return self._get_task_block(text, information)
        # return self._get_task_block2(text, information, sec_info)



    @staticmethod
    def _get_checkmark(task_completed: bool) -> str:
        if task_completed:
            return ":white_check_mark:"
        return ":white_large_square:"

    @staticmethod
    def _get_task_block(text, information):
        return [
            {"type": "section", "text": {"type": "mrkdwn", "text": text}},
            {"type": "context", "elements": [{"type": "mrkdwn", "text": information}]},
        ]

    @staticmethod
    def _get_task_block2(text, information, sec_info):
        return [
            {"type": "section", "text": {"type": "mrkdwn", "text": text}},
        ]



# {"type": "interactive_message", "attachments": [{"type": "button", "text": {"type": "plain_text","emoji": True,"text": "needs improvement"},"style": "danger","value": "good"}]},
# {"type": "button",
# "attachments":[{
# "callback_id":"button_cli",
# "attachment_type": "default",
# # [{
# "actions":
# [{
# "type": "button",
# "text":
# {"type": "plain_text","emoji": True,"text": "satisfactory"},
# "style": "primary","value": "bad"}]
# # }]
# }]
# },
#  {"type": "actions","elements": [{"type": "button", "text": {"type": "plain_text","emoji": True,"text": "needs improvement"},"style": "danger","value": "good", "action_id": "improv"}]},
# {"type": "actions", "elements": [{"type": "button", "text": {"type": "plain_text","emoji": True,"text": "satisfactory"},"style": "primary","value": "bad"}]},
