import discord
import config as cfg

bot = discord.Bot()


@bot.event
async def on_ready():
    print(f"I have successfully logged in as {bot.user}")

# ------------------------------ Application Management


@bot.slash_command(name="apply", description="Apply to become an internal tester")
async def apply(ctx):
    warning_text = cfg.WARNING_MESSAGE

    await ctx.respond(warning_text, view=application_confirm_view(), ephemeral=True, delete_after=60)


class apply_modal(discord.ui.Modal):
    """Defines the application form and what happens when you click submit"""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label=cfg.QUESTION_1, required=cfg.Q1_REQUIRED))
        self.add_item(discord.ui.InputText(label=cfg.QUESTION_2, required=cfg.Q2_REQUIRED))
        self.add_item(discord.ui.InputText(label=cfg.QUESTION_3, required=cfg.Q3_REQUIRED,
                                           style=discord.InputTextStyle.long))
        self.add_item(discord.ui.InputText(label=cfg.QUESTION_4, required=cfg.Q4_REQUIRED,
                                           style=discord.InputTextStyle.long))
        self.add_item(discord.ui.InputText(label=cfg.QUESTION_5, required=cfg.Q5_REQUIRED))

    async def callback(self, interaction: discord.Interaction):
        age = self.children[0].value
        timezone = self.children[1].value
        motivation = self.children[2].value
        experience = self.children[3].value
        commitment = self.children[4].value

        user = await bot.fetch_user(interaction.user.id)
        user_avatar = user.avatar.url

        application_title = "Internal Testing Application - " + user.display_name

        # create a neat little embed
        application_embed = discord.Embed(
            title=application_title,
            description="**Motivation**\n" + motivation + "\n\n**Experience**\n" + experience,
            color=discord.Colour.blurple(),
        )
        application_embed.add_field(name="Age", value=str(age))
        application_embed.add_field(name="Timezone", value=str(timezone), inline=True)
        application_embed.add_field(name="Commitment", value=str(commitment) + " (hours / month)", inline=True)
        application_embed.add_field(name="User ID", value=str(interaction.user.id), inline=True)
        application_embed.add_field(name="Joined Discord", value=str(interaction.user.created_at.date()), inline=True)

        application_embed.set_thumbnail(url=user_avatar)

        # Get the channel in whch the application summary is going to be posted
        channel = bot.get_channel(cfg.APPLICATION_REVIEW_CHANNEL)

        # Post the application summary embed
        app_message = await channel.send(view=application_manage_view(), embed=application_embed)

        # Create a thread on it so people can exchange in a nice and clean environment
        await channel.create_thread(name=application_title, message=app_message, auto_archive_duration=60,
                                    type=discord.ChannelType.public_thread, reason=None)

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
        candidate_id = self.reject_button_callback.view.message.embeds[0].fields[3].value

        # Send the user a congratulations message
        rejection_message = cfg.REJECTED_MESSAGE
        user = await bot.fetch_user(candidate_id)
        await user.send(rejection_message)

        await interaction.response.send_message("<@" + str(interaction.user.id) + "> rejected <@"
                                                + str(user.id) + ">'s application.")

    @discord.ui.button(label="Accept", custom_id="accept-button", style=discord.ButtonStyle.success)
    async def accept_button_callback(self, apply, interaction):
        self.disable_all_items()
        await self.message.edit(view=self)

        # Get the candidate ID from the application summary
        candidate_id = int(self.accept_button_callback.view.message.embeds[0].fields[3].value)

        # get server info
        guild = bot.get_guild(cfg.MONITORED_SERVER)
        # add role to candidate
        await guild.get_member(candidate_id).add_roles(guild.get_role(cfg.ROLE_TO_GIVE))

        # Send the user a congratulations message
        congrats_message = cfg.ACCEPTED_MESSAGE
        user = await bot.fetch_user(candidate_id)
        await user.send(congrats_message)

        await interaction.response.send_message("<@" + str(interaction.user.id) + "> accepted <@"
                                                + str(user.id) + ">'s application.")

# ------------------------------ Statistics command


@bot.slash_command(name="statistics", description="Messages sent per user in testing group")
async def statistics(ctx):

    result_dict = {}

    # get all the users who need to be monitored
    role_to_monitor = bot.get_guild(cfg.MONITORED_SERVER).get_role(cfg.MONITORED_ROLE)
    role_members = role_to_monitor.members
    for member in role_members:
        key = member.display_name + " (" + str(member.id) + " joined " + str(member.joined_at.date()) + ")"
        result_dict[key] = 0

    # get the number of messages per user in the monitored channel
    channel = bot.get_channel(cfg.MONITORED_CHANNEL)
    async for message in channel.history(limit=10000):
        key = message.author.display_name + " (" + str(message.author.id) + " joined " \
            + str(member.joined_at.date()) + ")"
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
bot.run(cfg.TOKEN)
