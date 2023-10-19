import discord
from core.classes import Cog_Extension
from discord import app_commands

class Help(Cog_Extension):
    @app_commands.command(name = "help", description = "Show how to use command.")
    async def help(self, interaction: discord.Interaction):
        embed=discord.Embed(title="Help", description="[see more](https://github.com/FuseFairy/DiscordBot-BardGPT/blob/main/README.md)\n\n**COMMANDS -**")
        embed.add_field(name="/bard_cookies", value="Set and delete your Google Bard Cookies.", inline=False)
        embed.add_field(name="/bard", value="Chat with Google Bard.", inline=False)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Help(bot))