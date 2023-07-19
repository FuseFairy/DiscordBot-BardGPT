import discord
import asyncio
import re
from bardapi import Bard
from src import log
from typing import Optional

logger = log.setup_logger(__name__)
using_func = {}

async def get_using_send(user_id):
    return using_func[user_id]

async def set_using_send(user_id, status: bool):
    using_func[user_id] = status

async def chatbot_ask(chatbot: Bard, message: str, image=None):
    loop = asyncio.get_running_loop()
    if image:
        result = await loop.run_in_executor(None, chatbot.ask_about_image, message, image)
    else:
        result = await loop.run_in_executor(None, chatbot.get_answer, message)
    return result

async def send_message(chatbot: Bard, interaction: discord.Interaction, user_message: str, image=None):
    using_func[interaction.user.id] = True
    reply = ''
    text = ''
    images_embed = []
    more_images_links = []
    more_images_embed = ''
    await interaction.response.defer(ephemeral=False, thinking=True)
    try:
        if image:
            reply = await chatbot_ask(chatbot, user_message, image)
        else:
            reply = await chatbot_ask(chatbot, user_message)

        # Get reply text
        text = f"{reply['content']}"
        text = re.sub(r'\[Image of[^\]]*?\].*?\n?', '', text)
        text = re.sub(r'\[[^\]]*?\\Images of[^\]]*?\].*?\n?', '', text)

        # Set the final message
        user_message = user_message.replace("\n", "")
        ask = f"> **{user_message}** - <@{str(interaction.user.id)}>\n\n"
        response = f"{ask}{text}"

        # Discord limit about 2000 characters for a message
        while len(response) > 2000:
            temp = response[:2000]
            response = response[2000:]
            await interaction.followup.send(temp)

        # Get the image, if available
        try:
            if ('' not in reply["images"] and len(reply["images"]) > 0) or len(reply["links"]) > 0:
                i = 1
                count = 0

                if len(reply["links"]) > 0:
                    images = reply["links"]
                else:
                    images = reply["images"]

                for image_link in images:
                    if len(images_embed) < 10:
                        images_embed.append(discord.Embed(url=f"https://bard.google.com/{i}").set_image(url=image_link))
                        count += 1
                        if count == 4:
                            i += 1
                            count = 0
                    else:
                        more_images_links.append(image_link)
                if len(more_images_links) > 0:
                    link_text = "\n\n".join(more_images_links)
                    if len(link_text) < 4096:
                        more_images_embed = discord.Embed(title= "More Links", description=link_text)
        except:
            pass
        else:
            if images_embed and more_images_embed:
                await interaction.followup.send(response, embeds=images_embed, wait=True)
                await interaction.followup.send(embed=more_images_embed, wait=True)
            elif images_embed:
                await interaction.followup.send(response, embeds=images_embed, wait=True)
            else:
                await interaction.followup.send(response, wait=True)
    except Exception as e:
            await interaction.followup.send(f">>> **Error while sending message: {e}**")
            logger.exception(f"Error while sending message: {e}")
    finally:
        using_func[interaction.user.id] = False