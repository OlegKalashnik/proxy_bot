from aiogram import Bot
from aiogram.dispatcher import Dispatcher

import asyncio

loop = asyncio.get_event_loop()

with open('telegrammT.txt', 'r', encoding='utf-8') as f:
    TOKEN = f.read().strip()

bot = Bot(token=TOKEN, loop=loop)
dp = Dispatcher(bot)
