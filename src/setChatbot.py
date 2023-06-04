import sqlite3
import discord
from src import log
from src.response import send_message
from Bard import Chatbot

logger = log.setup_logger(__name__)
users_chatbot = {}
default_id = None

########### mention chatbot setting ###########
async def set_chatbot(id):
    global chatbot
    global default_id
    default_id = id
    chatbot = Chatbot(session_id=default_id)

async def get_default_id():
    return default_id

async def get_chatbot():
    return chatbot

########### persinal chatbot setting ###########
class UserChatbot:
    def __init__(self, id: str):
        self.chatbot = Chatbot(session_id=id)

    async def send_message(self, interaction, message):
        await send_message(self.chatbot, interaction, message)

async def init_sql_chatbot():
    global users_chatbot
    try:
        with sqlite3.connect('Bard_id.db') as conn:
            cursor = conn.execute("SELECT user_id, secure_1psid from ID_DATA")
            for row in cursor:
                users_chatbot[row[0]] = UserChatbot(id=row[1])
    except Exception as e:
        logger.exception(f"Error while initial chatbot: {e}")

async def set_personal_chatbot(interaction: discord.Interaction, user_id: int, *, id: str=None):
    try:
        if id is None:
            id = default_id
            default_value = 1
        else:
            default_value = 0
        users_chatbot[user_id] = UserChatbot(id=id)
        with sqlite3.connect('Bard_id.db') as conn:
            c = conn.cursor()
            c.execute("INSERT OR REPLACE INTO ID_DATA (USER_ID, SECURE_1PSID, DEFAULT_VALUE) VALUES (?, ?, ?)", (user_id, id, default_value))
            conn.commit()
        logger.warning(f"\x1b[31m{interaction.user} set Google Bard successful\x1b[0m")
        return True
    except Exception as e:
        logger.exception(f"Error while set chatbot: {e}")
        return False

async def del_personal_chatbot(interaction: discord.Interaction, user_id):
    try:
        with sqlite3.connect('Bard_id.db') as conn:
            c = conn.cursor()
            c.execute("DELETE from ID_DATA where USER_ID = (?);", (user_id,))
            conn.commit()
        del users_chatbot[user_id]
        await interaction.followup.send("> **Delete finish.**")
        logger.warning(f"\x1b[31m{interaction.user} delete __Secure-1PSID\x1b[0m")
    except Exception as e:
        await interaction.followup.send(f">>> **Error while delete chatbot: {e}**")
        logger.exception(f"Error while delete chatbot: {e}")
    
async def update_id(new_id):
    with sqlite3.connect('Bard_id.db') as conn:
        cursor = conn.execute("SELECT user_id, default_value from ID_DATA")
        for row in cursor:
            if row[1] == '1':
                users_chatbot[row[0]] = UserChatbot(id=new_id)

async def get_users_chatbot():
    return users_chatbot