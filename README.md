# Prerequisites
You will need:
- pycord (latest)
- dotenv (latest)
- Python > 3.8

# Configuration
Config is entirely done by setting up an env file which should ahve the following fields:
- TOKEN -> the token of your bot as obtained from the discord developer portal
- APPLICATION_REVIEW_CHANNEL_ID -> where the application summaries will be sent once submitted
- MONITORED_CHANNEL -> the channel that will be monitored for activity

# Execution
All you need to execute the bot is python > 3.8.
Simply execute the bot.py file with `python bot.py` or `python3 bot.py` (while you are in the same directory as the file of course)
