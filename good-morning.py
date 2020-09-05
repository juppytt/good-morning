from flask import Flask, request, make_response, Response
import os
import json

from slackclient import SlackClient

# Your app's Slack bot user token
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
#SLACK_VERIFICATION_TOKEN = os.environ["SLACK_VERIFICATION_TOKEN"]

# Slack client for Web API requests
slack_client = SlackClient(SLACK_BOT_TOKEN)

# Flask web server for incoming traffic from Slack
app = Flask(__name__)

# Dictionary to store coffee orders. In the real world, you'd want an actual key-value store
WAKEUP_TIME = {}

# Send a message to the user asking if they would like coffee
user_id = "U019EJPBFFH"
channel_id = "C019NLH2ULE"

# Create a new order for this user in the WAKEUP_TIME dictionary
WAKEUP_TIME[user_id] = {
    "channel": channel_id,
    "time": {}
}

def gm_main():
    settime_dm = slack_client.api_call(
      "chat.postMessage",
      as_user=True,
      channel=channel_id,
        text="I am GoodMorning Bot :bee:, and I\'m here to help you wake up early :sunny:",
      attachments=[{
        "text": "",
        "callback_id": user_id + "set_time_form",
        "color": "#3AA3E3",
        "attachment_type": "default",
        "actions": [{
          "name": "set_time",
          "text": ":sunny: Set wake-up time",
          "type": "button",
          "value": "set_time"
        }]
      }]
    )

gm_main()


def set_time(user_id, trigger_id):
    # Add the message_ts to the user's order info
    print("set time!!")

    # Show the ordering dialog to the user
    open_dialog = slack_client.api_call(
        "dialog.open",
        trigger_id=trigger_id,
        dialog={
            "title": "Set wake-up time",
            "submit_label": "Submit",
            "callback_id": user_id + "set_time_form",
            "elements": [
                {
                    "label": "time",
                    "type": "text",
                    "name": "time",
                    "placeholder": "09:00",
                }
            ]
        }
    )

    #print(open_dialog)

    # Update the message to show that we're in the process of taking their order
    slack_client.api_call(
        "chat.postMessage",
        channel=WAKEUP_TIME[user_id]["channel"],
        text=":pencil: Taking your request...",
        attachments=[]
    )

@app.route("/slack/main", methods=["POST"])
def gm_main_called():
    gm_main()
    return make_response("", 200)

@app.route("/slack/check/time", methods=["POST"])
def check_time():
    # TODO: load database and return set time

@app.route("/slack/check/status", methods=["POST"])
    # TODO: load database and return status


@app.route("/slack/set", methods=["POST"])
def message_actions():
    # Parse the request payload

    message_action = request.form
    #message_action = json.loads(request.form["payload"])
    print(message_action)

    user_id = message_action["user_id"]
    trigger_id = message_action["trigger_id"]
    set_time(user_id, trigger_id)

    return make_response("", 200)

@app.route("/slack/interactive", methods=["POST"])
def interactive():
    message_action = json.loads(request.form["payload"])
    user_id= message_action["user"]["id"]
    print(message_action)

    if message_action["type"] == "interactive_message":
        trigger_id = message_action["trigger_id"]
        set_time(user_id, trigger_id)

    elif message_action["type"] == "dialog_submission":

        text=":white_check_mark: Wake-up time set!\n"
        text = text + "*" + message_action["user"]["name"] + "*"
        text = text + "'s wakeup-time: *" + message_action["submission"]["time"] + "*"


        # Update the message to show that we're in the process of taking their order
        slack_client.api_call(
            "chat.postMessage",
            channel=WAKEUP_TIME[user_id]["channel"],
            text = text,
            attachments=[]
        )


    return make_response("", 200)

if __name__ == "__main__":
    app.run()
