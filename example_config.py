# Necessary for the bot to function
TOKEN = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"


# ---------------------------- APPLICATION MANAGEMENT -------------------------

# The ID of the server you want to use the bot in (should be a numerical value)
MONITORED_SERVER = 000000000000000000

# Channel ID to which the application summaries will be sent (should be a numerical value)
APPLICATION_REVIEW_CHANNEL = 0000000000000000000

# Role ID to give to people whose applications you accept (should be a numerical value)
ROLE_TO_GIVE = 0000000000000000000

APPLICATION_COMMAND_DESCRIPTION = "Apply to become a Helldiver"

# Warning to give to user when he applies
WARNING_MESSAGE = "Please confirm that you understand that:\n\
        \n- This is not for the sole purpose of playing the game more often \
        \n- You will be expected to join in on at least some testing events \
        \n- If you do not participate in testing or provide feedback, your privileges may be revoked\n\n"

# Question 1  ---------------------------------------------  <- max length
QUESTION_1 = "How old are you?"
# Question 2  ---------------------------------------------  <- max length
QUESTION_2 = "What is your timezone? (in UTC format)"
# Question 3  ---------------------------------------------  <- max length
QUESTION_3 = "Why do you want to be an internal tester?"
# Question 4  ---------------------------------------------  <- max length
QUESTION_4 = "Do you have any previous tester experience?"
# Question 5  ---------------------------------------------  <- max length
QUESTION_5 = "How many hours per month can you commit?"

# Whether questions 1 through 5 are required or optional (write either True or False)
Q1_REQUIRED = True
Q2_REQUIRED = True
Q3_REQUIRED = True
Q4_REQUIRED = False
Q5_REQUIRED = True

# Message to send to applicant if application is ACCEPTED
ACCEPTED_MESSAGE = "Hi and thank you for applying to become an internal tester!\
        \nAfter careful consideration of your profile we have decided to accept your application.\
        \n\n:tada: Congratulations and welcome to the team! :tada:\
        \n\nYou should now have access to an extra channel in the server where you can interact with other testers.\
        \n\nWe are glad to have you on board and hope you can provide the team with valuable feedback!"

# Message to send to applicant if application is REJECTED
REJECTED_MESSAGE = "Hi and thank you for applying to become an internal tester.\
\nAfter careful consideration of your profile we have decided to not move forward with your application at \
this time.\
\nFeel free to contact a moderator if you have any further questions."

# ----------------------------- ACTIVITY MONITORING ---------------------------


# The role that is monitored for activity
MONITORED_ROLE = 0000000000000000000

# The channel that is monitored for activity
MONITORED_CHANNEL = 000000000000000000
