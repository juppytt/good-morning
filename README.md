![HEADER](https://github.com/juppytt/good-morning/blob/master/image/main.png)

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
[Main](https://github.com/juppytt/good-morning/blob/master/image/main.png)

[Set Time](https://github.com/juppytt/good-morning/blob/master/image/set-time.jpeg)


[Record Success](https://github.com/juppytt/good-morning/blob/master/image/record-success.jpeg)
[Record Fail](https://github.com/juppytt/good-morning/blob/master/image/record-fail.jpeg)

[Check All](https://github.com/juppytt/good-morning/blob/master/image/check-all.jpeg)

[Weekly Report](https://github.com/juppytt/good-morning/blob/master/image/weekly-report.jpeg)

[Request Skip](https://github.com/juppytt/good-morning/blob/master/image/request-skip.jpeg)
[Bank Alert](https://github.com/juppytt/good-morning/blob/master/image/bank-alert.jpeg)





