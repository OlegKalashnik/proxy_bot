from aiogram import types, Dispatcher
from create_bot import bot

from parse import parser


async def reboot_3proxy(callback_query: types.CallbackQuery):
    parser.get_connection()
    with open('id.txt', 'r', encoding='utf-8') as f:
        auth_users = f.readlines()
    trusted = False
    for user in auth_users:
        if str(callback_query.from_user.id) == user.strip():
            trusted = True
            break

    if trusted:
        await bot.send_message(
            callback_query.from_user.id,
            text=f'Перезагружаю 3roxy {callback_query.data.split("-")[1]} ...')
        await bot.send_message(
            callback_query.from_user.id,
            text=parser.reboot_3proxy(callback_query.data.split("-")[1]))
    else:
        await callback_query.answer('Тыщь пыщь тро-ло-ло!\nЯ водитель НЛО!')


def register_callback_handlers_reboot_3proxy(dp: Dispatcher):
    dp.register_callback_query_handler(reboot_3proxy, lambda c: c.data and c.data.startswith('reboot_3proxy'))
