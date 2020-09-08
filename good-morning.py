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
#user_id = "U019EJPBFFH"

#test channel
#channel_id = "C019NLH2ULE"

#fame user_id
user_id = "U0123456789"

#GoodMorning channel
channel_id = 'C019ZB2HK38'

# Create a new order for this user in the WAKEUP_TIME dictionary
WAKEUP_TIME = {
    "channel": channel_id,
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
            "name": "record_time",
            "text": ":sunny: Record wake-up time",
            "type": "button",
            "value": "record_time"
        },
        {
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
        },
        {
            "name": "check_score",
            "text": ":bookmark: Check wake-up mission score",
            "type": "button",
            "value": "check_score"
        }]

      }]
    )

#gm_main()

def set_time(user_id, trigger_id, user_name, time=""):
    # Add the message_ts to the user's order info
    print("set time: " + time)

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
                    "placeholder": "09:00"
                }
            ]
        }
    )

    # Update the message to show that we're in the process of taking their order
    text=":pencil: [" + user_name +"] Taking your request..."
    slack_client.api_call(
        "chat.postMessage",
        channel=WAKEUP_TIME["channel"],
        text=text,
        attachments=[]
    )

def check_time(user_id, user_name):

    res = db.get_time_db(user_id)
    if (res == ""):
        return make_response("", 500)

    text = ":sunny: *" + user_name + "*'s wake-up time: *" + res + "*"
    slack_client.api_call(
        "chat.postMessage",
        channel=WAKEUP_TIME["channel"],
        text = text,
        attachments=[]
    )

    return make_response("", 200)

def record_time(user_id, user_name):
    res, time = db.record_time_db(user_id, user_name)

    text = ""
    if (res < 0):
        text = text + ":cloud: *" + user_name + "*, you woke up late today :( "
    else:
        text = text +":sunny: *" + user_name + "*, good morning! "
    text = text + " wake-up time: *" + time + "*"
    slack_client.api_call(
        "chat.postMessage",
        channel=WAKEUP_TIME["channel"],
        text = text,
        attachments=[]
    )
    return make_response("", 200)

def check_score(user_id, user_name):

    res = db.get_record_db(user_id)

    text = ":sunny: *" + user_name + "*'s wake-up score: \n"
    text = text + res
    slack_client.api_call(
        "chat.postMessage",
        channel=WAKEUP_TIME["channel"],
        text = text,
        attachments=[]
    )

    return make_response("", 200)


# weekly report
def weekly_report():
    message_action = request.form
    print(message_action)

    res = db.get_weekly_db()

    slack_client.api_call(
        "chat.postMessage",
        channel=WAKEUP_TIME["channel"],
        text = res,
        attachments=[]
    )

    db.erase_record_db()

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

@app.route("/slack/check/score", methods=["POST"])
def slash_check_score():
    # Parse the request payload
    message_action = request.form
    print(message_action)

    user_id = message_action["user_id"]
    user_name = message_action["user_name"]
    return check_score(user_id, user_name)



# from /set slash command
@app.route("/slack/set", methods=["POST"])
def slash_set_time():
    message_action = request.form
    print(message_action)

    user_id = message_action["user_id"]
    trigger_id = message_action["trigger_id"]
    user_name = message_action["user_name"]
    time = message_action["text"]
    set_time(user_id, trigger_id, user_name, time)

    return make_response("", 200)

@app.route("/slack/rmv", methods=["POST"])
def slash_rmv_user():
    message_action = request.form
    print(message_action)
    return make_response("", 200)


# record wake-up time
@app.route("/slack/record", methods=["POST"])
def slash_record():
    message_action = request.form
    print(message_action)

    user_id = message_action["user_id"]
    user_name = message_action["user_name"]

    return record_time(user_id, user_name)


## Slack interactive
@app.route("/slack/interactive", methods=["POST"])
def interactive():
    message_action = json.loads(request.form["payload"])
    user_id= message_action["user"]["id"]
    user_name = message_action["user"]["name"]
    print(message_action)

    message_type = message_action["type"]
    if message_type == "interactive_message":
        trigger_id = message_action["trigger_id"]
        action_name = message_action["actions"][0]["name"]
        if action_name == "set_time":
            set_time(user_id, trigger_id, user_name)
        elif action_name == "check_time":
            check_time(user_id, user_name)
        elif action_name == "record_time":
            return record_time(user_id, user_name)

        elif action_name == "check_score":
            return check_score(user_id, user_name)


    elif message_type == "dialog_submission":
        time = message_action["submission"]["time"]
        if (db.set_time_db(user_id, time) < 0):
            text = ":warning: Error... Contact the admin please :("
            slack_client.api_call(
                "chat.postMessage",
                channel=WAKEUP_TIME["channel"],
                text = text,
                attachments=[]
            )
            return make_response("", 500)
        try:
            db.set_user_name_db(user_id, user_name)
        except:
            print("set_user_name error")

        text=":white_check_mark: ["+ user_name +"] Wake-up time set!\n"
        text = text + ":sunny: *" + user_name + "*"
        text = text + "'s wake-up time: *" + time + "*"

        # Update the message to show that we're in the process of taking their order
        slack_client.api_call(
            "chat.postMessage",
            channel=WAKEUP_TIME["channel"],
            text = text,
            attachments=[]
        )


    return make_response("", 200)


## Slack interactive
@app.route("/slack/event", methods=["POST"])
def event():
    slack_event = json.loads(request.data)
    print(slack_event)
    if ("challenge" in slack_event):
        return make_response(slack_event["challenge"], 200,
                             {"content-type": "application/json"})
    event_type = slack_event["event"]["type"]
    user_id = slack_event["authed_users"][0]
    if (event_type == "channel_left"):
        db.rmv_db_user(user_id)
    elif (event_type == "member_joined_channel"):
        db.add_db_user(user_id)
    elif (event_type == "app_mention"):
        weekly_report()

    return make_response("", 200)

if __name__ == "__main__":
    app.run()
