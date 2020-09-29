from flask import Flask, request, make_response, Response
import os
import json
import db
from apscheduler.schedulers.background import BackgroundScheduler
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
channel_id = "C019NLH2ULE"

#fame user_id
user_id = "U0123456789"

#GoodMorning channel
#channel_id = 'C019ZB2HK38'

# Create a new order for this user in the WAKEUP_TIME dictionary
WAKEUP_TIME = {
    "channel": channel_id,
}


## Good morning common functions

def gm_main():
    gm_message = slack_client.api_call(
      "chat.postMessage",
      as_user=True,
      channel=channel_id,
        text="I am GoodMorning Bot :sunrise:, and I\'m here to help you wake up early :simple_smile:",
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
            "name": "set_skip",
            "text": ":last_quarter_moon_with_face: Skip tomorrow",
            "type": "button",
            "value": "set_skip"
        },
        {
            "name": "check_top",
            "text": ":bookmark: Check my...",
            "type": "button",
            "value": "check_top"
        }
        ]

      }]
    )
    return make_response("", 200)
def gm_check():
    gm_message = slack_client.api_call(
      "chat.postMessage",
      as_user=True,
      channel=channel_id,
        text=":bookmark: What do you want to check? ",
      attachments=[{
        "text": "",
        "callback_id": user_id + "set_time_form",
        "color": "#3AA3E3",
        "attachment_type": "default",
        "actions": [{
            "name": "check_time",
            "text": ":bookmark: Check my wake-up time",
            "type": "button",
            "value": "check_time"
        },
        {
            "name": "check_score",
            "text": ":bookmark: Check my score",
            "type": "button",
            "value": "check_score"
        },
        {
            "name": "check_penalty",
            "text": ":date: Weekly Report",
            "type": "button",
            "value": "check_penalty"
        },
        {
            "name": "check_balance",
            "text": ":money_with_wings: Check my balance",
            "type": "button",
            "value": "check_balance"
        }]
      }]
    )
    return make_response("", 200)


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

def set_skip(user_id, user_name):
    print("set skip: " + user_name)
    res = db.record_skip_db(user_id, user_name)
    text = ":last_quarter_moon_with_face: *" + user_name + "* requested skip for tomorrow."
    slack_client.api_call(
        "chat.postMessage",
        channel=WAKEUP_TIME["channel"],
        text = text,
        attachments=[]
    )

    if res == db.ERROR_SKIPPED_BEFORE:
        text = ":no_entry: Sorry! You already skipped once this week."
    elif res == db.ERROR_SKIP_LATE:
        text = ":no_entry: Sorry! It's too late to skip."
    else:
        text = ":heavy_check_mark: Okay! You can take a break tomorrow."
    slack_client.api_call(
        "chat.postMessage",
        channel=WAKEUP_TIME["channel"],
        text = text,
        attachments=[]
    )

    return make_repsonse("", 200)
def check_time(user_id, user_name):

    res = db.get_time_db(user_id)
    if (res == ""):
        return make_response("", 500)

    text = ":sunrise: *" + user_name + "*'s wake-up time: *" + res + "*"
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

    text = ":blossom: *" + user_name + "*'s wake-up score: \n"
    text = text + res
    slack_client.api_call(
        "chat.postMessage",
        channel=WAKEUP_TIME["channel"],
        text = text,
        attachments=[]
    )

    return make_response("", 200)

def check_balance(user_id, user_name):
    res = db.get_balance_db(user_id)
    text = ":money_with_wings: *" + user_name + "*'s balance:   "
    text = text + res + "\n"
    slack_client.api_call(
        "chat.postMessage",
        channel=WAKEUP_TIME["channel"],
        text = text,
        attachments=[]
    )

    return make_response("", 200)

def slack_user_name(user_id):
    try:
        # Get user name from slack
        response = slack_client.api_call(
            "users.info",
            user=user_id
        )
        #print(response)
        if response["ok"] == False:
            return ""

        return response["user"]["real_name"]
    except:
        return ""


# weekly report (penalty report)
def penalty_report():

    res = "*Weekly Report!*\n"
    res = res + db.get_weekly_db()

    slack_client.api_call(
        "chat.postMessage",
        channel=WAKEUP_TIME["channel"],
        text = res,
        attachments=[]
    )

    return make_response("", 200)


def flush_weekly():
    res = db.update_penalty_db()
    db.erase_record_db()
    if res is not "":
        slack_client.api_call(
            "chat.postMessage",
            channel=WAKEUP_TIME["channel"],
            text = res,
            attachments=[]
        )


def set_real_name():
    res = db.dump_db(db.DB_REC, db.fname_rec)
    for i in range(len(res)):
        data = res[i]
        user_id = data["User Id"]
        real_name = slack_user_name(user_id)
        data["User Name"] = real_name
        db.set_user_name_db(user_id, real_name)
    res = db.get_weekly_db()
    print(res)

# process user message for mission
def process_user_message(slack_event, user_id, user_name):
    file_type = slack_event["event"]["files"][0]["filetype"]
    print(file_type)
    if (file_type == "jpg" or file_type == "jpeg"):
        record_time(user_id, user_name)
## Slack slash commands

# Slack bot help message
@app.route("/slack/help", methods=["POST"])
def gm_main_called():
    return gm_main()

@app.route("/slack/check/time", methods=["POST"])
def slash_check_time():
    # Parse the request payload
    message_action = request.form
    print(message_action)

    user_id = message_action["user_id"]
    user_name = message_action["user_name"]
    real_name = slack_user_name(user_id)
    return check_time(user_id, real_name)

@app.route("/slack/check/score", methods=["POST"])
def slash_check_score():
    # Parse the request payload
    message_action = request.form
    print(message_action)

    user_id = message_action["user_id"]
    user_name = message_action["user_name"]
    real_name = slack_user_name(user_id)
    return check_score(user_id, real_name)



# from /set slash command
@app.route("/slack/set", methods=["POST"])
def slash_set_time():
    message_action = request.form
    print(message_action)

    user_id = message_action["user_id"]
    trigger_id = message_action["trigger_id"]
    user_name = message_action["user_name"]
    time = message_action["text"]
    real_name = slack_user_name(user_id)
    set_time(user_id, trigger_id, real_name, time)

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
    real_name = slack_user_name(user_id)
    return record_time(user_id, real_name)


## Slack interactive
@app.route("/slack/interactive", methods=["POST"])
def interactive():
    message_action = json.loads(request.form["payload"])
    user_id= message_action["user"]["id"]
    user_name = message_action["user"]["name"]
    real_name = slack_user_name(user_id)
    print(message_action)

    message_type = message_action["type"]
    if message_type == "interactive_message":
        trigger_id = message_action["trigger_id"]
        action_name = message_action["actions"][0]["name"]
        if action_name == "set_time":
            set_time(user_id, trigger_id, real_name)
        elif action_name == "check_time":
            check_time(user_id, real_name)
        elif action_name == "record_time":
            return record_time(user_id, real_name)
        elif action_name == "check_top":
            return gm_check()
        elif action_name == "check_score":
            return check_score(user_id, real_name)
        elif action_name == "check_penalty":
            return penalty_report()
        elif action_name == "check_balance":
            return check_balance(user_id, real_name)
        elif action_name == "set_skip":
            return set_skip(user_id, real_name)

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
            db.set_user_name_db(user_id, real_name)
        except:
            print("set_user_name error")

        text=":white_check_mark: ["+ real_name +"] Wake-up time set!\n"
        text = text + ":sunny: *" + real_name + "*"
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

    print("\n /slack/event")
    print(slack_event)

    if ("challenge" in slack_event):
        return make_response(slack_event["challenge"], 200,
                             {"content-type": "application/json"})
    event_type = slack_event["event"]["type"]
    try:
        user_id = slack_event["event"]["user"]
        user_name = slack_user_name(user_id)
        print("user_name: ")
        print(user_name)
    except:
        return make_response("", 200)

    if (event_type == "channel_left"):
        db.rmv_db_user(user_id)
    elif (event_type == "member_joined_channel"):
        db.add_db_user(user_id)
    elif (event_type == "message"):
        if (slack_event["event"]["channel"] == channel_id):
            if ("files" in slack_event["event"]):
                process_user_message(slack_event, user_id, user_name)

    #elif (event_type == "app_mention"):
    #    text = slack_event["event"]["text"]
    #    if "Weekly" in text or "weekly" in text:
    #        penalty_report()

    return make_response("", 200)

### Schduler
scheduler = BackgroundScheduler()

job = scheduler.add_job(gm_main, 'cron',
                           day_of_week = "mon,tue,wed,thu,fri",
                           hour = 8,
                           id = 'help')
job = scheduler.add_job(penalty_report, 'cron',
                           day_of_week = "fri",
                           hour = 12,
                           id = 'weekly')

# Flush weekly records on every Saturday 10PM
job = scheduler.add_job(flush_weekly, 'cron',
                        day_of_week = 'sat',
                        hour = 22,
                        id = 'flush_weekly')

scheduler.start()

if __name__ == "__main__":
    app.run()
