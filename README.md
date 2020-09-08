# good-morning
slack bot for wake-up mission


## Requirements
* python packages
    * flask
    * json
    * slackclient
    * datetime
    * csv

* ngrok (with account)
* Your own Slack app & SLACK_BOT_TOKEN

## Commands
* `/help`
* `/set`
* `/goodmorning`
* `/check-time`
* `/check-score`


## INSTALL
1. Prepare your own Slack App (https://slack.com/intl/en-kr/help/articles/115005265703-Create-a-bot-for-your-workspace)
2. Run `python good-morning.py` with your SLACK_BOT_TOKEN. This will run a flask server
3. Get public URL of your server (I used `ngrok`) 
4. Go to Slack app settings. Set Interactivity, Slash Commands, OAuth&Permissions, and Event Subscribtions with your server URL.
