![HEADER](github.com/juppytt/good-morning/blob/master/image/main.png)

# good-morning :sunrise: 
A Slack Bot for wake up mission


## Requirements
* python2.7
* python packages
    * APScheduler
    * Flask
    * slackclient
    * holidays

* ngrok (with account)
* Your own Slack app & SLACK_BOT_TOKEN

## INSTALL
1. Prepare your own Slack App (https://slack.com/intl/en-kr/help/articles/115005265703-Create-a-bot-for-your-workspace)
2. Run `python good-morning.py` with your SLACK_BOT_TOKEN. This will run a flask server.
3. Get public URL of your server (I used `ngrok`) 
4. Go to Slack app settings. Set Interactivity, Slash Commands, OAuth&Permissions, and Event Subscribtions with your server URL.


## EXAMPLE
[Main](github.com/juppytt/good-morning/blob/master/image/main.png)

[Set Time](github.com/juppytt/good-morning/blob/master/image/set-time.jpeg)


[Record Success](github.com/juppytt/good-morning/blob/master/image/record-success.jpeg)
[Record Fail](github.com/juppytt/good-morning/blob/master/image/record-fail.jpeg)

[Check All](github.com/juppytt/good-morning/blob/master/image/check-all.jpeg)

[Weekly Report](github.com/juppytt/good-morning/blob/master/image/weekly-report.jpeg)

[Request Skip](github.com/juppytt/good-morning/blob/master/image/request-skip.jpeg)
[Bank Alert](github.com/juppytt/good-morning/blob/master/image/bank-alert.jpeg)





