import discord
import re
import os
import asyncio
import requests
from bardapi import Bard
from src.mention_chatbot import MentionChatbot
from src import log
from dotenv import load_dotenv
from discord.ext import commands
from core.classes import Cog_Extension

load_dotenv()

chatbot = MentionChatbot()
image_extensions = ('.jpg', '.jpeg', '.png', '.webp')

try:
    MENTION_CHANNEL_ID = int(os.getenv("MENTION_CHANNEL_ID"))
except:
    MENTION_CHANNEL_ID = None
logger = log.setup_logger(__name__)
sem = asyncio.Semaphore(1)

class Event(Cog_Extension):
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        image_bytes = None
        if message.author == self.bot.user:
            return
        if self.bot.user in message.mentions:
            if not MENTION_CHANNEL_ID or message.channel.id == MENTION_CHANNEL_ID:
                content = re.sub(r'<@.*?>', '', message.content).strip()
                if len(content) > 0:
                    username = str(message.author)
                    channel = str(message.channel)
                    logger.info(f"\x1b[31m{username}\x1b[0m : '{content}' ({channel})")

                    for image in message.attachments:
                        if image.filename.endswith(image_extensions):
                            image_bytes = requests.get(image).content
                            break
                    if image_bytes:
                        await chatbot.send_message(message, content, image_bytes)
                    else:
                        await chatbot.send_message(message, content)
            elif MENTION_CHANNEL_ID is not None:
                await message.channel.send(f"> **Can only be mentioned at <#{self.bot.get_channel(MENTION_CHANNEL_ID).id}>**")

async def setup(bot):
    await bot.add_cog(Event(bot))