import discord
import requests
from discord import app_commands
from core.classes import Cog_Extension
from src import log
from src.personal_chatbot import get_personal_chatbots, set_personal_chatbot
from typing import Optional

logger = log.setup_logger(__name__)
image_extensions = ['.jpg', '.jpeg', '.png', '.webp']

class Bard(Cog_Extension):
    # Set and delete chatbot.
    @app_commands.command(name="chatbot_setting", description="Set or delete Google Bard token(__Secure-1PSID).")
    @app_commands.choices(choice=[app_commands.Choice(name="set", value="set"), app_commands.Choice(name="delete", value="delete")])
    async def cookies_setting(self, interaction: discord.Interaction, choice: app_commands.Choice[str], secure_1psid: str=None):
        await interaction.response.defer(ephemeral=True, thinking=True)
        personal_chatbots = await get_personal_chatbots()
        user_id = interaction.user.id
        if choice.value == "set":
            try:
                await set_personal_chatbot(user_id, secure_1psid)
                if secure_1psid:
                    await interaction.followup.send("> **INFO: Set chatbot successfull!**")
                else:
                    await interaction.followup.send("> **INFO: Set chatbot successfull! (using default token)**")
            except Exception as e:
                await interaction.followup.send(f"> **ERROR: {e}**")
        elif choice.value == "delete":
            try:
                if user_id in personal_chatbots:
                    await personal_chatbots[user_id].del_chatbot()
                    await interaction.followup.send("> **INFO: Delete chatbot successful!**")
            except Exception as e:
                await interaction.followup.send(f"> **ERROR: {e}**")

    # Chat with Google Bard.
    @app_commands.command(name="bard", description="Have a chat with Google Bard")
    async def bard(self, interaction: discord.Interaction, image: Optional[discord.Attachment]=None, *, message: str):
        personal_chatbots = await get_personal_chatbots()
        username = str(interaction.user)
        channel = str(interaction.channel)
        user_id = interaction.user.id
        if user_id not in personal_chatbots:
            await interaction.response.defer(ephemeral=True, thinking=True)
            await interaction.followup.send("> **ERROR: Please use  `/set_chatbot`  to set yourself chatbot first.**")
        logger.info(f"\x1b[31m{username}\x1b[0m : '{message}' ({channel})")
        if image is not None:
            file_extension = image.filename[image.filename.rfind('.'):].lower()
            if file_extension in image_extensions:
                image_bytes = requests.get(image).content
                await personal_chatbots[user_id].send_message(interaction, message, image_bytes)
            else:
                await interaction.response.defer(ephemeral=True, thinking=True)
                await interaction.followup.send("> **ERROR: This file format is not supported**")
        else:
            await personal_chatbots[user_id].send_message(interaction, message)

async def setup(bot):
    await bot.add_cog(Bard(bot))
