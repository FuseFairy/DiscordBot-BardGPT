import discord
import asyncio
import re
from bardapi import Bard
from src import log

logger = log.setup_logger(__name__)

async def chatbot_ask(chatbot: Bard, message: str, image=None):
    loop = asyncio.get_running_loop()
    if image:
        result = await loop.run_in_executor(None, chatbot.ask_about_image, message, image)
    else:
        result = await loop.run_in_executor(None, chatbot.get_answer, message)
    return result

async def send_message(chatbot: Bard, interaction, user_message: str, image=None):
    reply = ''
    text = ''
    ask = ''
    images_embed = []
    more_images_links = []
    more_images_embed = ''
    if isinstance(interaction, discord.Interaction):
        await interaction.response.defer(ephemeral=False, thinking=True)
    elif isinstance(interaction, discord.message.Message):
        await interaction.channel.typing()
    try:
        if image:
            reply = await chatbot_ask(chatbot, user_message, image)
        else:
            reply = await chatbot_ask(chatbot, user_message)

        # Get reply text
        text = f"{reply['content']}"
        text = re.sub(r'\[Image of[^\]]*?\].*?\n?', '', text)
        text = re.sub(r'\[\d+\s+Images\s+of\s+[^\]]*\]', '', text)

        # Set the final message
        if isinstance(interaction, discord.Interaction):
            user_message = user_message.replace("\n", "")
            ask = f"> **{user_message}** - <@{str(interaction.user.id)}>\n\n"
        response = f"{ask}{text}"

        # Discord limit about 2000 characters for a message
        while len(response) > 2000:
            temp = response[:2000]
            response = response[2000:]
            if isinstance(interaction, discord.Interaction):
                await interaction.followup.send(temp)
            elif isinstance(interaction, discord.message.Message):
                await interaction.channel.send(temp)

        # Get the image, if available
        if (len(reply["images"]) > 0 and reply["images"][0] != ""):
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
                if len(link_text) < 4096:
                    more_images_embed = discord.Embed(title= "More Links", description=link_text)

        if len(images_embed) > 0 and len(more_images_embed) > 0:
            if isinstance(interaction, discord.Interaction):
                await interaction.followup.send(response, embeds=images_embed, wait=True)
                await interaction.followup.send(embed=more_images_embed, wait=True)
            elif isinstance(interaction, discord.message.Message):
                await interaction.channel.send(text, embeds=images_embed)
                await interaction.channel.send(embed=more_images_embed)
        elif len(images_embed) > 0:
            if isinstance(interaction, discord.Interaction):
                await interaction.followup.send(response, embeds=images_embed, wait=True)
            elif isinstance(interaction, discord.message.Message):
                await interaction.channel.send(text, embeds=images_embed)
        else:
            if isinstance(interaction, discord.Interaction):
                await interaction.followup.send(response, wait=True)
            elif isinstance(interaction, discord.message.Message):
                await interaction.channel.send(text)
    except Exception as e:
            if isinstance(interaction, discord.Interaction):
                await interaction.followup.send(f">>> **ERROR: {e}**")
            elif isinstance(interaction, discord.message.Message):
                await interaction.channel.send(f">>> **ERROR: {e}**")
            logger.exception(f"Error: {e}")