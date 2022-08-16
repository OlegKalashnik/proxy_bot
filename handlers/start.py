from aiogram import types, Dispatcher
from keyboards import inline_servers
from parse import parser


# @dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    with open('id.txt', 'r', encoding='utf-8') as f:
        auth_users = f.readlines()
    trusted = False
    for user in auth_users:
        if str(message.from_user.id) == user.strip():
            trusted = True
            break

    if trusted:
        parser.run()
        await message.answer('Доступные сервера', reply_markup=inline_servers)
    else:
        await message.answer('Тыщь пыщь тро-ло-ло!\nЯ водитель НЛО!')


def register_message_handlers_start(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'Servers'])
