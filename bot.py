import dotenv
from os import getenv
import discord

# Load environment variables
dotenv.load_dotenv()
# the bot's auth token
TOKEN = getenv("TOKEN")
# channel in which moderators will see applications
APPLICATION_REVIEW_CHANNEL = int(getenv("APPLICATION_REVIEW_CHANNEL"))
# Role to give to users who succeed with their application
ROLE_TO_GIVE = int(getenv("ROLE_TO_GIVE"))
# Monitored server ID
MONITORED_SERVER = int(getenv("MONITORED_SERVER"))
# Monitored channel
MONITORED_CHANNEL = int(getenv("MONITORED_CHANNEL"))
# Monitored role
MONITORED_ROLE = int(getenv("MONITORED_ROLE"))

bot = discord.Bot()


@bot.event
async def on_ready():
    print(f"I have successfully logged in as {bot.user}")


# ------------------------------ Application Management

@bot.slash_command(name="apply", description="Apply to become an internal tester")
async def apply(ctx):
    warning_text = "Please confirm that you understand that:\n\
        \n- This is not for the sole purpose of playing the game more often \
        \n- You will be expected to join in on at least some testing events \
        \n- If you do not participate in testing or provide feedback, your privileges may be revoked\n\n"

    await ctx.respond(warning_text, view=application_confirm_view(), ephemeral=True, delete_after=60)


class apply_modal(discord.ui.Modal):
    """Defines the application form and what happens when you click submit"""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="How old are you?", required=True))
        self.add_item(discord.ui.InputText(label="What is your timezone? (in UTC format)", required=True))
        self.add_item(discord.ui.InputText(label="Why do you want to be an internal tester?", required=True, style=discord.InputTextStyle.long))
        self.add_item(discord.ui.InputText(label="Do you have any previous tester experience?", required=True, style=discord.InputTextStyle.long))
        self.add_item(discord.ui.InputText(label="How many hours per month can you commit?", required=True))

    async def callback(self, interaction: discord.Interaction):
        age = self.children[0].value
        timezone = self.children[1].value
        justification = self.children[2].value
        experience = self.children[3].value
        commitment = self.children[4].value

        user = await bot.fetch_user(interaction.user.id)
        user_avatar = user.avatar.url

        application_title = "Internal Testing Application - " + user.display_name

        # create a neat little embed
        application_embed = discord.Embed(
            title=application_title,
            description=justification,
            color=discord.Colour.blurple(),
        )
        application_embed.add_field(name="Age", value=str(age))
        application_embed.add_field(name="Timezone", value=str(timezone), inline=True)
        application_embed.add_field(name="Commitment", value=str(commitment) + " (hours per month)", inline=True)
        application_embed.add_field(name="Experience", value=str(experience))
        application_embed.add_field(name="User ID", value=str(interaction.user.id), inline=True)
        application_embed.add_field(name="Joined Discord", value=str(interaction.user.created_at.date()), inline=True)

        application_embed.set_thumbnail(url=user_avatar)

        # Get the channel in whch the application summary is going to be posted
        channel = bot.get_channel(APPLICATION_REVIEW_CHANNEL)

        # Post the application summary embed
        app_message = await channel.send(view=application_manage_view(), embed=application_embed)

        # Create a thread on it so people can exchange in a nice and clean environment
        await channel.create_thread(name=application_title, message=app_message, auto_archive_duration=60, type=discord.ChannelType.public_thread, reason=None)

        thank_you_message = "Thank you for applying! A staff member will get back to you shortly."
        await interaction.response.send_message(thank_you_message, ephemeral=True)


class application_confirm_view(discord.ui.View):
    """Defines the confirmation message when applying"""

    @discord.ui.button(label="Nevermind", style=discord.ButtonStyle.danger)
    async def cancel_button_callback(self, apply, interaction):
        await interaction.response.send_message("You cancelled your application.", ephemeral=True)

    @discord.ui.button(label="I understand", style=discord.ButtonStyle.success)
    async def confirm_button_callback(self, apply, interaction):
        await interaction.response.send_modal(apply_modal(title="Apply for internal tester position"))


class application_manage_view(discord.ui.View):
    """Adds button to application summary so admins/moderators can accept or reject candidates quicker"""
    def __init__(self):
        super().__init__(timeout=None)  # timeout of the view must be set to None

    @discord.ui.button(label="Reject", custom_id="reject-button", style=discord.ButtonStyle.danger)
    async def reject_button_callback(self, apply, interaction):
        self.disable_all_items()
        await self.message.edit(view=self)

        # Get the candidate ID from the application summary
        candidate_id = self.reject_button_callback.view.message.embeds[0].fields[4].value

        # Send the user a congratulations message
        rejection_message = "Hi and thank you for applying to become an internal tester for EXFIL.\
        \nAfter careful consideration of your profile we have decided to not move forward with your application at this time.\
        \nFeel free to contact a moderator if you have any further questions."
        user = await bot.fetch_user(candidate_id)
        await user.send(rejection_message)

        await interaction.response.send_message("<@" + str(interaction.user.id) + "> rejected the application for candidate <@" + str(user.id) + ">.")

    @discord.ui.button(label="Accept", custom_id="accept-button", style=discord.ButtonStyle.success)
    async def accept_button_callback(self, apply, interaction):
        self.disable_all_items()
        await self.message.edit(view=self)

        # Get the candidate ID from the application summary
        candidate_id = int(self.accept_button_callback.view.message.embeds[0].fields[4].value)

        # get server info
        guild = bot.get_guild(MONITORED_SERVER)
        # add role to candidate
        await guild.get_member(candidate_id).add_roles(guild.get_role(ROLE_TO_GIVE))

        # Send the user a congratulations message
        congrats_message = "Hi and thank you for applying to become an internal tester for EXFIL.\
        \nAfter careful consideration of your profile we have decided to accept your application.\
        \n\n:tada: Congratulations and welcome to the team! :tada:\
        \n\nYou should now have access to an extra channel in the server where you can interact with other testers.\
        \n\nWe are glad to have you on board and hope you can provide the team with valuable feedback!"
        user = await bot.fetch_user(candidate_id)
        await user.send(congrats_message)

        await interaction.response.send_message("<@" + str(interaction.user.id) + "> accepted the application for candidate <@" + str(user.id) + ">.")

# ------------------------------ Statistics command


@bot.slash_command(name="statistics", description="Messages sent per user in testing group")
async def statistics(ctx):

    result_dict = {}

    # get all the users who need to be monitored
    role_to_monitor = bot.get_guild(MONITORED_SERVER).get_role(MONITORED_ROLE)
    role_members = role_to_monitor.members
    for member in role_members:
        key = member.display_name + " (" + str(member.id) + " joined " + str(member.joined_at.date()) + ")"
        result_dict[key] = 0

    # get the number of messages per user in the monitored channel
    channel = bot.get_channel(MONITORED_CHANNEL)
    async for message in channel.history(limit=10000):
        key = message.author.display_name + " (" + str(message.author.id) + " joined " + str(member.joined_at.date()) + ")"
        # ignore users who are not in the monitored role
        if key in result_dict:
            result_dict[key] += 1

    # sort dictionary
    result_dict = dict(sorted(result_dict.items(), key=lambda item: item[1]))

    # print it prettily
    result_summary = ""
    for key in result_dict:
        result_summary += key + ": " + str(result_dict[key]) + "\n"

    await ctx.respond(result_summary, ephemeral=True)

# launch the bot
bot.run(TOKEN)
