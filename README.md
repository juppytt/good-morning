![HEADER](https://github.com/juppytt/good-morning/blob/master/image/main.png)

# :sunny: good-morning 
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
### Main
![Main](https://github.com/juppytt/good-morning/blob/master/image/main.png)
Default set to post main message on *every weekday 8 AM*.

### Set Time
![Set Time](https://github.com/juppytt/good-morning/blob/master/image/set-time.jpeg)
Users can set their wake up time *once in a week*.

### Record Wake up Time
![Record Success](https://github.com/juppytt/good-morning/blob/master/image/record-success.jpeg)
![Record Fail](https://github.com/juppytt/good-morning/blob/master/image/record-fail.jpeg)

### Check

![Check All](https://github.com/juppytt/good-morning/blob/master/image/check-all.jpeg)


### Weekly Report
![Weekly Report](https://github.com/juppytt/good-morning/blob/master/image/weekly-report.jpeg)
Default set to post weekly report on *every Friday 12 PM*.

### Skip Request
![Request Skip](https://github.com/juppytt/good-morning/blob/master/image/request-skip.jpeg)
Users can request to skip the mission on the following day. 
By default, skip is accpeted only *before 10PM* and *once in a week*. 

### Bank Alert
![Bank Alert](https://github.com/juppytt/good-morning/blob/master/image/bank-alert.jpeg)
By default, good-morning calculates the fee and rewards and penalties on /*Friday 12:05PM*/. 
For those with negative deposits, the bank posts an alert message. 
