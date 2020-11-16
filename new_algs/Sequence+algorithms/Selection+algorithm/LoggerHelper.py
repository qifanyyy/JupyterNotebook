from slackclient import SlackClient

from config import SLACK_TOKEN


class Logger:
    sc = SlackClient(SLACK_TOKEN)

    @staticmethod
    def send(msg):
        # Logger.sc.api_call(
        #     "chat.postMessage",
        #     channel="#ades-bot",
        #     text=msg
        # )
        print(msg)

    @staticmethod
    def send_channel_grid_search(msg):
        Logger.sc.api_call(
            "chat.postMessage",
            channel="#ades-grid-search",
            text=msg
        )
        print(msg)

    @staticmethod
    def send_personal(msg):
        Logger.sc.api_call(
            "chat.postMessage",
            channel="@luismelo7",
            text=msg
        )
        print(msg)
