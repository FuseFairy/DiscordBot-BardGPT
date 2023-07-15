import discord
import asyncio
import re
from bardapi import Bard
from src import log

logger = log.setup_logger(__name__)
using_func = {}

async def get_using_send(user_id):
    return using_func[user_id]

async def set_using_send(user_id, status: bool):
    using_func[user_id] = status

async def chatbot_ask(chatbot: Bard, message: str):
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(None, chatbot.get_answer, message)
    return result

async def send_message(chatbot: Bard, interaction: discord.Interaction, user_message: str):
    using_func[interaction.user.id] = True
    reply = ''
    text = ''
    images_embed = []
    more_images_links = []
    more_images_embed = ''
    await interaction.response.defer(ephemeral=False, thinking=True)
    try:
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
                        more_images_links.append(image_link)
                if len(more_images_links) > 0:
                    link_text = "\n\n".join(more_images_links)
                    more_images_embed = discord.Embed(title= "More Images", description=link_text)
        except:
            pass
        else:
            if images_embed and more_images_links:
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