![HEADER](juppytt.github.com/good-morning/image/main.png)

# good-morning 
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
[Main](juppytt.github.com/good-morning/image/main.png)

[Set Time](juppytt.github.com/good-morning/image/set-time.jpeg)


[Record Success](juppytt.github.com/good-morning/image/record-success.jpeg)
[Record Fail](juppytt.github.com/good-morning/image/record-fail.jpeg)

[Check All](juppytt.github.com/good-morning/image/check-all.jpeg)

[Weekly Report](juppytt.github.com/good-morning/image/weekly-report.jpeg)

[Request Skip](juppytt.github.com/good-morning/image/request-skip.jpeg)
[Bank Alert](juppytt.github.com/good-morning/image/bank-alert.jpeg)





