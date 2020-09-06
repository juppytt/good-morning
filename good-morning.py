from flask import Flask, request, make_response, Response
import os
import json
import db

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


## Good morning common functions

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
            "text": ":memo: Set wake-up time",
            "type": "button",
            "value": "set_time"
        },
        {
            "name": "check_time",
            "text": ":bookmark: Check wake-up time",
            "type": "button",
            "value": "check_time"
        }]
      }]
    )

#gm_main()

def set_time(user_id, trigger_id, user_name):
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

    # Update the message to show that we're in the process of taking their order
    text=":pencil: [" + user_name +"] Taking your request..."
    slack_client.api_call(
        "chat.postMessage",
        channel=WAKEUP_TIME[user_id]["channel"],
        text=text,
        attachments=[]
    )

def check_time(user_id, user_name):

    res = db.get_time_db(user_id)
    if (res < 0):
        return make_response("", 500)

    text = ":sunny: *" + user_name + "*'s wake-up time: *" + res + "*"
    slack_client.api_call(
        "chat.postMessage",
        channel=WAKEUP_TIME[user_id]["channel"],
        text = text,
        attachments=[]
    )

    return make_response("", 200)

def record(user_id, user_name):
    return make_response("", 200)

## Slack slash commands

# Slack bot help message
@app.route("/slack/help", methods=["POST"])
def gm_main_called():
    gm_main()
    return make_response("", 200)

@app.route("/slack/check/time", methods=["POST"])
def slash_check_time():
    # Parse the request payload
    message_action = request.form
    print(message_action)

    user_id = message_action["user_id"]
    user_name = message_action["user_name"]
    return check_time(user_id, user_name)

#@app.route("/slack/check/status", methods=["POST"])
    # TODO: load database and return status


# from /set slash command
@app.route("/slack/set", methods=["POST"])
def slash_set_time():
    message_action = request.form
    print(message_action)

    user_id = message_action["user_id"]
    trigger_id = message_action["trigger_id"]
    user_name = message_action["user_name"]
    set_time(user_id, trigger_id, user_name)

    return make_response("", 200)

# record wake-up time
@app.route("/slack/record", methods=["POST"])
def slash_record():
    message_action = request.form
    print(message_action)

    user_id = message_action["user_id"]
    user_name = message_action["user_name"]

    return record(user_id, user_name)


## Slack interactive

@app.route("/slack/interactive", methods=["POST"])
def interactive():
    message_action = json.loads(request.form["payload"])
    user_id= message_action["user"]["id"]
    user_name = message_action["user"]["name"]
    print(message_action)

    if message_action["type"] == "interactive_message":
        trigger_id = message_action["trigger_id"]
        action_name = message_action["actions"][0]["name"]
        if (action_name == "set_time"):
            set_time(user_id, trigger_id, user_name)
        elif (action_name == "check_time"):
            check_time(user_id, user_name)

    elif message_action["type"] == "dialog_submission":

        time = message_action["submission"]["time"]
        if (db.set_time_db(user_id, time) < 0):
            text = ":warning: Error... Contact the admin please :("
            slack_client.api_call(
                "chat.postMessage",
                channel=WAKEUP_TIME[user_id]["channel"],
                text = text,
                attachments=[]
            )
            return make_response("", 500)

        text=":white_check_mark: ["+ user_name +"] Wake-up time set!\n"
        text = text + ":sunny: *" + user_name + "*"
        text = text + "'s wakeup-time: *" + time + "*"

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
