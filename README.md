# Features

## Application Management
The bot lets people use the /apply command to apply for a role.
1. The would-be candidate first receives a warning to avoid people who would spam the application:
![image](https://github.com/user-attachments/assets/ed76216f-39e3-4792-be6e-816452eb995f)
2. Once the user selects that they have understood the terms they are met with a form to fill:
![image](https://github.com/user-attachments/assets/2e214a31-5e49-49b0-8c5b-5a21884fd83e)
3. Once the application is submitted it is formatted and the information provided is sent to a private channel specified in the configuration (`APPLICATION_REVIEW_CHANNEL_ID`).
A thread is also automatically created as well as `Accept` and `Reject` buttons.
![image](https://github.com/user-attachments/assets/51112723-0b69-4c80-a959-dd7f7a18e6c7)
4. As soon as either the Accept or Reject buttons are pressed:
    - The candidate receives a confirmation or rejection message via direct message
    - A confirmation message is printed in the application review channel that clearly states who did the action on which candidate
    - If the accept button was pressed, the candidate is automatically given the role defined in the configuration (`ROLE_TO_GIVE`).


## Activity Monitoring
The bot allows a user to check who among a specific role (`MONITORED_ROLE`) has been active in a channel specified in the configuration (`MONITORED_CHANNEL`).
It will then send an ephemeral (visible only to the user who launched the command) message with the list of users, when they joined, and how many messages they have sent in the specified channel.

# Self Hosting the bot
## Prerequisites
You will need:
- [pycord](https://pycord.dev/) (latest)
- [Python](https://www.python.org/) > 3.8

## Configuration
Config is entirely done by setting up a python `config.py` file.
You can find an example config file in the same directory as the bot named `example_config.py`.
All the fields should be explained in comments in the file.
Simply rename the file to `config.py` and add in all the missing information or feel free to modify the default contents.

## Execution
Simply execute the bot.py file with `python bot.py` or `python3 bot.py` (while you are in the same directory as the file of course)
