import discord
import requests
from discord import app_commands
from core.classes import Cog_Extension
from src import log
from src.setChatbot import set_personal_chatbot, del_personal_chatbot, get_users_chatbot, get_default_session_id, reset_user_chatbot
from src.response import get_using_send, set_using_send
from typing import Optional

logger = log.setup_logger(__name__)
image_extensions = ['.jpg', '.jpeg', '.png', '.webp']

class BardGPT(Cog_Extension):
    # Chat with Google Bard
    @app_commands.command(name="bard", description="Have a chat with Google Bard")
    async def bard(self, interaction: discord.Interaction, image: Optional[discord.Attachment]=None, *, message: str):
        try:
            using = await get_using_send(interaction.user.id)
        except:
            await set_using_send(interaction.user.id, False)
            using = await get_using_send(interaction.user.id)
        finally:
            if not using:
                users_chatbot = await get_users_chatbot()
                username = str(interaction.user)
                usermessage = message
                channel = str(interaction.channel)
                user_id = interaction.user.id
                if user_id not in users_chatbot:
                    if await get_default_session_id() is None:
                        await interaction.response.defer(ephemeral=True, thinking=True)
                        await interaction.followup.send("> **Bot owner should use !bardupload command to set \_\_Secure-1PSID first, or you can use /bard_cookies command to set your \_\_Secure-1PSID.**")
                    else:
                        if await set_personal_chatbot(interaction, user_id) is not True:
                            await interaction.response.defer(ephemeral=True, thinking=True)
                            await interaction.followup.send(">>> **Error while set chatbot**")
                        else:
                            users_chatbot = await get_users_chatbot()
                logger.info(f"\x1b[31m{username}\x1b[0m : '{usermessage}' ({channel})")
                if image is not None:
                    file_extension = image.filename[image.filename.rfind('.'):].lower()
                    if file_extension in image_extensions:
                        image_bytes = requests.get(image).content
                        await users_chatbot[user_id].send_message(interaction, usermessage, image_bytes)
                    else:
                        await interaction.response.defer(ephemeral=True, thinking=True)
                        await interaction.followup.send("> **This file format is not supported**")
                else:
                    await users_chatbot[user_id].send_message(interaction, usermessage)
            else:
                await interaction.response.defer(ephemeral=True, thinking=True)
                await interaction.followup.send("> **Please wait for your last conversation to finish.**")
            

    # Set and delete personal Google bard Cookies
    @app_commands.command(name="bard_cookies", description="Set or delete Google Bard __Secure-1PSID")
    @app_commands.choices(choice=[app_commands.Choice(name="set", value="set"), app_commands.Choice(name="delete", value="delete")])
    async def cookies_setting(self, interaction: discord.Interaction, choice: app_commands.Choice[str], secure_1psid: str=None):
        await interaction.response.defer(ephemeral=True, thinking=True)
        user_id = interaction.user.id
        if choice.value == "set":
            if secure_1psid is None:
                await interaction.followup.send("> **Error while set chatbot: Please input your \_\_Secure-1PSID**")
            else:
                if await set_personal_chatbot(interaction, user_id=user_id, session_id=secure_1psid):
                    await interaction.followup.send("> **Upload successful!**")
                else:
                    await interaction.followup.send(">>> **Error while set chatbot**")
                    
        elif choice.value == "delete":
            if user_id in await get_users_chatbot():
                await del_personal_chatbot(interaction, user_id=user_id)
            else:
                await interaction.followup.send("> **Error while delete chatbot: You don't have any chatbot**")
    
    @app_commands.command(name="reset_bard_conversation", description="Reset Bard chatbot conversation")
    async def bard_reset(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True, thinking=True)
        user_id = interaction.user.id
        await reset_user_chatbot(user_id)
        await interaction.followup.send("> **Reset finish!**")

async def setup(bot):
    await bot.add_cog(BardGPT(bot))
