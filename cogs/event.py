import discord
import re
import os
import asyncio
from Bard import Chatbot
from src.response import chatbot_ask
from src.setChatbot import get_chatbot, get_default_id
from src import log
from dotenv import load_dotenv
from discord.ext import commands
from core.classes import Cog_Extension

load_dotenv()

chatbot = None

try:
    MENTION_CHANNEL_ID = int(os.getenv("MENTION_CHANNEL_ID"))
except:
    MENTION_CHANNEL_ID = None
logger = log.setup_logger(__name__)
sem = asyncio.Semaphore(1)

async def send_message(chatbot: Chatbot, message: discord.message.Message, user_message: str):
    async with sem:
        await message.channel.typing()
        reply = ''
        text = ''
        images_embed = []
        try:
            reply = await chatbot_ask(chatbot, user_message)   

            # Get reply text
            text = f"{reply['content']}"
            text = re.sub(r'\[Image of[^\]]*?\].*?\n?', '', text)

            # Set the final message
            user_message = user_message.replace("\n", "")

            # Discord limit about 2000 characters for a message
            while len(text) > 2000:
                temp = text[:2000]
                text = text[2000:]
                await message.channel.send(temp)

            # Get the image, if available
            try:
                if reply["images"] != "set()":
                    i = 1
                    count = 0
                    for image_link in reply["images"]:
                        if len(images_embed) < 10:
                            images_embed.append(discord.Embed(url=f"https://bard.google.com/{i}").set_image(url=image_link))
                            count += 1
                            if count == 4:
                                i += 1
                                count = 0
                        else:
                            break
            except:
                pass
            else:
                if images_embed:
                    await message.channel.send(text, embeds=images_embed)
                else:
                    await message.channel.send(text)
        except Exception as e:
                await message.channel.send(f">>> **Error: {e}**")
                logger.exception(f"Error while sending message: {e}")

class Event(Cog_Extension):
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        if self.bot.user in message.mentions:
            if await get_default_id() is None:
                await message.channel.typing()
                await message.channel.send(f"> **Bot owner should use !upload command to set __Secure-1PSID first.**")
            else:
                if not MENTION_CHANNEL_ID or message.channel.id == MENTION_CHANNEL_ID:
                    content = re.sub(r'<@.*?>', '', message.content).strip()
                    if len(content) > 0:
                        chatbot = await get_chatbot()
                        username = str(message.author)
                        channel = str(message.channel)
                        logger.info(f"\x1b[31m{username}\x1b[0m : '{content}' ({channel})")
                        task = asyncio.create_task(send_message(chatbot, message, content))
                        await asyncio.gather(task)
                elif MENTION_CHANNEL_ID is not None:
                    await message.channel.send(f"> **Can only be mentioned at <#{self.bot.get_channel(MENTION_CHANNEL_ID).id}>**")

async def setup(bot):
    await bot.add_cog(Event(bot))