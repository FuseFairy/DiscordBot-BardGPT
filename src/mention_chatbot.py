import os
from asyncio import Semaphore
from src import log
from src.response import send_message
from bardapi import Bard
from dotenv import load_dotenv

load_dotenv()

logger = log.setup_logger(__name__)

class MentionChatbot():
    def __init__(self):
        self.sem = Semaphore(1)
        self.chatbot = Bard(token=os.getenv("___SECURE_1PSID"))

    async def send_message(self, message, content, image=None):
        async with self.sem:
            if image:
                await send_message(self.chatbot, message, content, image)
            else:
                await send_message(self.chatbot, message, content)