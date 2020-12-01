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


## Screenshots
### Main
![Main](https://github.com/juppytt/good-morning/blob/master/image/main.png) 
Default set to post main menu message on **every weekday 8 AM**.

### Set Time
![Set Time](https://github.com/juppytt/good-morning/blob/master/image/set-time.png | width=100) 
You can set your wake up time **once in a week**.

### Wake up Mission
![Record Success](https://github.com/juppytt/good-morning/blob/master/image/record-success.png | width=150) 
![Record Fail](https://github.com/juppytt/good-morning/blob/master/image/record-fail.jpeg | width=150)  

To success at the wake up mission, just send a photo on the slack channel before your wake up time. It's Super EASY!:simple_smile:  

### Check

![Check All](https://github.com/juppytt/good-morning/blob/master/image/check-all.jpeg) 


### Weekly Report
![Weekly Report](https://github.com/juppytt/good-morning/blob/master/image/weekly-report.png | width=150)  
Weekly report shows the weekly score of the participants and their penalty/reward.  
Default set to post weekly report on **every Friday 12 PM**. 

### Skip Request
![Request Skip](https://github.com/juppytt/good-morning/blob/master/image/request-skip.jpeg | width=150 )
Users can request to skip the mission on the following day.  
By default, skip is accpeted only **before 10PM** and **once in a week**.  

### Bank Alert
![Bank Alert](https://github.com/juppytt/good-morning/blob/master/image/bank-alert.jpeg )
By default, good-morning calculates the fee and rewards and penalties on **Friday 12:05PM**.  
For those with negative deposits, the bank posts an alert message. 
