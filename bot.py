import discord
import os
import src.log
import sqlite3
import pkg_resources
from src.personal_chatbot import init_personal_chatbots
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# init loggger
logger = src.log.setup_logger(__name__)

conn = sqlite3.connect('Bard_id.db')
c = conn.cursor()
try:
    c.execute('''CREATE TABLE ID_DATA
                 (USER_ID INT PRIMARY KEY NOT NULL,
                 TOKEN  TEXT NOT NULL,
                 USE_DEFAULT_COOKIE  INT DEFAULT 0);''')
    conn.commit()
    conn.close()
except:
    pass

def check_version():
    required = [line.strip() for line in open('requirements.txt')]

    for package in required:
        package_name, package_version = package.split('==')
        name, version = pkg_resources.get_distribution(package_name).project_name, pkg_resources.get_distribution(package_name).version
        if package != f'{name}=={version}':
            raise ValueError(f'{name} version {version} is installed but does not match the requirements')

@bot.event
async def on_ready():
    bot_status = discord.Status.online
    bot_activity = discord.Activity(type=discord.ActivityType.playing, name="/help")
    await bot.change_presence(status=bot_status, activity=bot_activity)
    await init_personal_chatbots()
    for Filename in os.listdir('./cogs'):
        if Filename.endswith('.py'):
            await bot.load_extension(f'cogs.{Filename[:-3]}')  
    logger.info(f'{bot.user} is now running!')
    print("Bot is Up and Ready!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)

# Load command
@commands.is_owner()
@bot.command(name="bardload")
async def load(ctx, extension):
    await bot.load_extension(f'cogs.{extension}')
    await ctx.author.send(f'> **Loaded {extension} done.**')

# Unload command
@commands.is_owner()
@bot.command(name="bardunload")
async def unload(ctx, extension):
    await bot.unload_extension(f'cogs.{extension}')
    await ctx.author.send(f'> **Un-Loaded {extension} done.**')

# Empty discord_bot.log file
@commands.is_owner()
@bot.command(name="bardclean")
async def clean(ctx):
    open('discord_bot.log', 'w').close()
    await ctx.author.send(f'> **Successfully emptied the file!**')

# Get discord_bot.log file
@commands.is_owner()
@bot.command(name="bardgetLog")
async def getLog(ctx):
    try:
        with open('discord_bot.log', 'rb') as f:
            file = discord.File(f)
        await ctx.author.send(file=file)
    except:
        await ctx.author.send("> **Send failed!**")

# Get Bard_id.db file
@commands.is_owner()
@bot.command(name="bardgetdb")
async def getdb(ctx):
    try:
        with open('Bard_id.db', 'rb') as f:
            file = discord.File(f)
        await ctx.author.send(file=file)
    except:
        await ctx.author.send("> **Send failed!**")

if __name__ == '__main__':
    check_version()
    bot.run(os.getenv("DISCORD_BOT_TOKEN"))