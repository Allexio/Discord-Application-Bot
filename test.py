import dotenv
from os import getenv
import discord
import json

# Load environment variables
dotenv.load_dotenv()
# the bot's auth token
token = str(getenv("TOKEN"))
# channel in which moderators will see applications
application_review_channel = str(getenv("APP_REVIEW_CHANNEL"))
# role to be given out if the application is accepted
role_to_join = str(getenv("ROLE_TO_JOIN"))

bot = discord.Bot()

applications = json.load()


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
        self.add_item(discord.ui.InputText(label="How many hours per month do you think you can commit for testing?", required=True))

    async def callback(self, interaction: discord.Interaction):
        age = self.children[0].value
        timezone = self.children[1].value
        justification = self.children[2].value
        commitment = self.children[3].value
        thank_you_message = "Thank you for applying! A staff member will get back to you shortly."
        await interaction.response.send_message(thank_you_message, ephemeral=True)


class application_confirm_view(discord.ui.View):
    @discord.ui.button(label="Nevermind", style=discord.ButtonStyle.danger)
    async def cancel_button_callback(self, apply, interaction):
        self.disable_all_items()
        await interaction.response.send_message("You cancelled your application.", ephemeral=True)

    @discord.ui.button(label="I understand", style=discord.ButtonStyle.success)
    async def confirm_button_callback(self, apply, interaction):
        self.disable_all_items()
        await interaction.response.send_modal(apply_modal(title="Apply for internal tester position"))


try:
    # run the bot
    bot.run(token)
except KeyError:
    print("FATAL: Could not find the token environment variable")
