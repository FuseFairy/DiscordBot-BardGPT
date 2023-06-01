import discord
import json
from Bard import Chatbot
from typing import Optional
from discord import app_commands
from core.classes import Cog_Extension
from src import log
from src.response import send_message, get_using_send, set_using_send

logger = log.setup_logger(__name__)

users_chatbot = {}

async def init_chatbot(user_id):
    with open("./cookies.json", encoding="utf-8") as f:
        cookies_json = json.load(f)
    users_chatbot[user_id] = UserChatbot(cookies_json)

class UserChatbot:
    def __init__(self, cookies):
        for cookie in cookies:
            if cookie.get("name") == "__Secure-1PSID":
               id = cookie.get("value")
               break
        self.chatbot = Chatbot(session_id=id)

    async def send_message(self, interaction, message):
        await send_message(self.chatbot, interaction, message)

class BardGPT(Cog_Extension):
    # Chat with Google Bard
    @app_commands.command(name="bard", description="Have a chat with Google Bard")
    async def bard(self, interaction: discord.Interaction, *, message: str):
        try:
            using = await get_using_send(interaction.user.id)
        except:
            await set_using_send(interaction.user.id, False)
            using = await get_using_send(interaction.user.id)
        if not using: 
            username = str(interaction.user)
            usermessage = message
            channel = str(interaction.channel)
            user_id = interaction.user.id
            if user_id not in users_chatbot:
                await init_chatbot(user_id)
            await interaction.response.defer(ephemeral=False, thinking=True)
            logger.info(f"\x1b[31m{username}\x1b[0m : '{usermessage}' ({channel})")
            await users_chatbot[user_id].send_message(interaction, usermessage)
        else:
            await interaction.response.defer(ephemeral=True, thinking=True)
            await interaction.followup.send("> **Please wait for your last conversation to finish.**")

    # Set and delete personal Google bard Cookies
    @app_commands.command(name="bard_cookies", description="Set or delete Google Bard Cookies")
    @app_commands.choices(choice=[app_commands.Choice(name="set", value="set"), app_commands.Choice(name="delete", value="delete")])
    async def cookies_setting(self, interaction: discord.Interaction, choice: app_commands.Choice[str], cookies_file: Optional[discord.Attachment]=None):
        await interaction.response.defer(ephemeral=True, thinking=True)
        user_id = interaction.user.id
        if choice.value == "set":
            try:
                content = json.loads(await cookies_file.read())
                users_chatbot[user_id] = UserChatbot(cookies=content)
                await interaction.followup.send("> **Upload successful!**")
                logger.warning(f"\x1b[31m{interaction.user} set Google Bard Cookies successful\x1b[0m")
            except:
                await interaction.followup.send("> **Please upload your Google Bard Cookies.**")
        else:
            try:
                del users_chatbot[user_id]
                await interaction.followup.send("> **Delete finish.**")
                logger.warning(f"\x1b[31m{interaction.user} delete Cookies\x1b[0m")
            except:
                await interaction.followup.send("> **You don't have any Google Bard Cookies.**")

async def setup(bot):
    await bot.add_cog(BardGPT(bot))