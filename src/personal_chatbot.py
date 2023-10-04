import sqlite3
import os
from asyncio import Semaphore
from src.response import send_message
from src import log
from bardapi import Bard
from dotenv import load_dotenv

load_dotenv()

logger = log.setup_logger(__name__)
sem = Semaphore(1)
personal_chatbots = {}

async def set_personal_chatbot(user_id, token=None):
    async with sem:
        if token:
            use_default_cookie = 0
        else:
            use_default_cookie = 1
            token = os.getenv('___SECURE_1PSID')

        personal_chatbots[user_id] = PersonalChatbot(user_id, token, use_default_cookie)
        with sqlite3.connect('Bard_id.db') as conn:
                c = conn.cursor()
                c.execute("INSERT OR REPLACE INTO ID_DATA (USER_ID, TOKEN, USE_DEFAULT_COOKIE) VALUES (?, ?, ?)", (user_id, token, use_default_cookie))
                conn.commit()

async def get_personal_chatbots():
    return personal_chatbots

async def init_personal_chatbots():
    with sqlite3.connect('Bard_id.db') as conn:
        cursor = conn.execute("SELECT USER_ID, TOKEN, USE_DEFAULT_COOKIE from ID_DATA")
        for row in cursor:
            try:
                personal_chatbots[row[0]] = PersonalChatbot(row[0], row[1], row[2])
            except Exception as e:
                logger.exception(f"Error while initial chatbot: {e} ({row[0]})")

class PersonalChatbot():
    def __init__(self, user_id, token, use_default_cookie):
        self.sem = Semaphore(1)
        self.user_id = user_id
        self.token = token
        self.use_default_cookie = use_default_cookie
        self.chatbot = Bard(token=self.token)

    async def send_message(self, interaction, message, image=None):
        async with self.sem:
            if image:
                await send_message(self.chatbot, interaction, message, image)
            else:
                await send_message(self.chatbot, interaction, message)

    async def del_chatbot(self):
        with sqlite3.connect('Bard_id.db') as conn:
            c = conn.cursor()
            c.execute("DELETE from ID_DATA where USER_ID = (?);", (self.user_id,))
            conn.commit()
        del personal_chatbots[self.user_id]