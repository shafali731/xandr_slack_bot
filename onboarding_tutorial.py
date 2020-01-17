# {
#     "channel": "D0123456",
#     "username": "pythonboardingbot",
#     "icon_emoji": ":robot_face:",
#     "blocks": [
#         {
#             "type": "section",
#             "text": {
#                 "type": "mrkdwn",
#                 "text": "Welcome to Slack! :wave: We're so glad you're here. :blush:\n\n*Get started by completing the steps below:*",
#             },
#         },
#         {"type": "divider"},
#         {
#             "type": "section",
#             "text": {
#                 "type": "mrkdwn",
#                 "text": ":white_large_square: *Add an emoji reaction to this message* :thinking_face:\nYou can quickly respond to any message on Slack with an emoji reaction. Reactions can be used for any purpose: voting, checking off to-do items, showing excitement.",
#             },
#         },
#         {
#             "type": "context",
#             "elements": [
#                 {
#                     "type": "mrkdwn",
#                     "text": " :information_source: *<https://get.slack.help/hc/en-us/articles/206870317-Emoji-reactions|Learn How to Use Emoji Reactions>*",
#                 }
#             ],
#         },
#         {"type": "divider"},
#         {
#             "type": "section",
#             "text": {
#                 "type": "mrkdwn",
#                 "text": ":white_large_square: *Pin this message* :round_pushpin:\nImportant messages and files can be pinned to the details pane in any channel or direct message, including group messages, for easy reference.",
#             },
#         },
#         {
#             "type": "context",
#             "elements": [
#                 {
#                     "type": "mrkdwn",
#                     "text": " :information_source: *<https://get.slack.help/hc/en-us/articles/205239997-Pinning-messages-and-files|Learn How to Pin a Message>*",
#                 }
#             ],
#         },
#     ],
# }

class OnboardingTutorial:
    """Constructs the onboarding message and stores the state of which tasks were completed."""

    # TODO: Create a better message builder:
    # https://github.com/slackapi/python-slackclient/issues/392
    # https://github.com/slackapi/python-slackclient/pull/400
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

#     Y_N = {
# 	"blocks": [
# 		{
# 			"type": "section",
# 			"text": {
# 				"type": "mrkdwn",
# 				"text": "You have a new request:\n*<fakeLink.toEmployeeProfile.com|Fred Enriquez - New device request>*"
# 			}
# 		},
# 		{
# 			"type": "section",
# 			"fields": [
# 				{
# 					"type": "mrkdwn",
# 					"text": "*Type:*\nComputer (laptop)"
# 				},
# 				{
# 					"type": "mrkdwn",
# 					"text": "*When:*\nSubmitted Aut 10"
# 				},
# 				{
# 					"type": "mrkdwn",
# 					"text": "*Last Update:*\nMar 10, 2015 (3 years, 5 months)"
# 				},
# 				{
# 					"type": "mrkdwn",
# 					"text": "*Reason:*\nAll vowel keys aren't working."
# 				},
# 				{
# 					"type": "mrkdwn",
# 					"text": "*Specs:*\n\"Cheetah Pro 15\" - Fast, really fast\""
# 				}
# 			]
# 		},
# 		{
# 			"type": "actions",
# 			"elements": [
# 				{
# 					"type": "button",
# 					"text": {
# 						"type": "plain_text",
# 						"emoji": True,
# 						"text": "Approve"
# 					},
# 					"style": "primary",
# 					"value": "click_me_123"
# 				},
# 				{
# 					"type": "button",
# 					"text": {
# 						"type": "plain_text",
# 						"emoji": True,
# 						"text": "Deny"
# 					},
# 					"style": "danger",
# 					"value": "click_me_123"
# 				}
# 			]
# 		}
# 	]
# }

    def __init__(self, channel):
        self.channel = channel
        self.username = "feedbackbot"
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
                self.DIVIDER_BLOCK,
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
        return self._get_task_block(text, information)

    # def _get_checkboxes(self):
    #     text = (
    #         f"{task_checkmark} *Pin this message* :round_pushpin:\n"
    #         "Important messages and files can be pinned to the details pane in any channel or"
    #         " direct message, including group messages, for easy reference."
    #     )
    #     attachments =  (
    #         "text": "Choose a game to play",
    #         "fallback": "You are unable to choose a game",
    #         "callback_id": "wopr_game",
    #         "color": "#3AA3E3",
    #         "attachment_type": "default",
    #         "actions": [
    #             {
    #                 "name": "game",
    #                 "text": "Chess",
    #                 "type": "button",
    #                 "value": "chess"
    #             },
    #             {
    #                 "name": "game",
    #                 "text": "Falken's Maze",
    #                 "type": "button",
    #                 "value": "maze"
    #             }
    #             ])

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
