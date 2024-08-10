import dotenv
from os import getenv
import discord

# Load environment variables
dotenv.load_dotenv()
# the bot's auth token
TOKEN = getenv("TOKEN")
# channel in which moderators will see applications
APPLICATION_REVIEW_CHANNEL_ID = int(getenv("APPLICATION_REVIEW_CHANNEL_ID"))
# role to be given out if the application is accepted
ROLE_TO_JOIN = getenv("ROLE_TO_JOIN")

bot = discord.Bot()


@bot.event
async def on_ready():
    print(f"I have successfully logged in as {bot.user}")


@bot.slash_command(name="apply-for-internal-tester", description="Apply to become an internal tester")
async def apply(ctx):
    warning_text = "Please confirm that you understand that:\n\
        \n- This is not for the sole purpose of playing the game more often \
        \n- You will be expected to join in on at least some testing events \
        \n- If you do not participate in testing or provide feedback, your privileges may be revoked\n\n"

    await ctx.respond(warning_text, view=application_confirm_view(), ephemeral=True)


class apply_modal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(discord.ui.InputText(label="How old are you?", required=True))
        self.add_item(discord.ui.InputText(label="What is your timezone? (in UTC format)", required=True))
        self.add_item(discord.ui.InputText(label="Why do you want to be an internal tester?", required=True, style=discord.InputTextStyle.long))
        self.add_item(discord.ui.InputText(label="How many hours per month can you commit?", required=True))

    async def callback(self, interaction: discord.Interaction):
        age = self.children[0].value
        timezone = self.children[1].value
        justification = self.children[2].value
        commitment = self.children[3].value

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

        application_embed.set_thumbnail(url=user_avatar)

        # Get the channel in whch the application summary is going to be posted
        channel = bot.get_channel(APPLICATION_REVIEW_CHANNEL_ID)

        # Post the application summary embed
        app_message = await channel.send(embed=application_embed)

        # Create a thread on it so people can exchange in a nice and clean environment
        await channel.create_thread(name=application_title, message=app_message, auto_archive_duration=60, type=discord.ChannelType.public_thread, reason=None)

        thank_you_message = "Thank you for applying! A staff member will get back to you shortly."
        await interaction.response.send_message(thank_you_message, ephemeral=True)


class application_confirm_view(discord.ui.View):
    @discord.ui.button(label="Nevermind", style=discord.ButtonStyle.danger)
    async def cancel_button_callback(self, apply, interaction):
        await interaction.response.send_message("You cancelled your application.", ephemeral=True)

    @discord.ui.button(label="I understand", style=discord.ButtonStyle.success)
    async def confirm_button_callback(self, apply, interaction):
        await interaction.response.send_modal(apply_modal(title="Apply for internal tester position"))


# launch the bot
bot.run(TOKEN)
