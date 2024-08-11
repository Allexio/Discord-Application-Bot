# Features

## Application Management
The bot lets people use the /apply command to apply for a role.
Once the application is submitted it is formatted and the information provided is sent to a private channel specified in the configuration (`APPLICATION_REVIEW_CHANNEL_ID`).

## Activity Monitoring
The bot allows a user to check who has been active in a channel specified in the configuration (`MONITORED_CHANNEL`).
It will then send an ephemeral (visible only to the user who launched the command) message with the list of users and how many messages they have sent in the specified channel.

# Self Hosting the bot
## Prerequisites
You will need:
- [pycord](https://pycord.dev/) (latest)
- [dotenv](https://pypi.org/project/python-dotenv/) (latest)
- [Python](https://www.python.org/) > 3.8

## Configuration
Config is entirely done by setting up an env file which should have the following fields:
- `TOKEN` -> the token of your bot as obtained from the discord developer portal
- `APPLICATION_REVIEW_CHANNEL_ID` -> where the application summaries will be sent once submitted
- `MONITORED_CHANNEL` -> the channel that will be monitored for activity

## Execution
All you need to execute the bot is python > 3.8.
Simply execute the bot.py file with `python bot.py` or `python3 bot.py` (while you are in the same directory as the file of course)
