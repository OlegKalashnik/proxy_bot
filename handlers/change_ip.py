from aiogram import types, Dispatcher
from create_bot import bot

from parse import parser


async def change_ip(callback_query: types.CallbackQuery):
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
            text=f'Меняю ай-пи на {callback_query.data.split("-")[2]} ...')
        await bot.send_message(
            callback_query.from_user.id,
            text=parser.change_ip(callback_query.data.split("-")[1], callback_query.data.split("-")[2]))
    else:
        await callback_query.answer('Тыщь пыщь тро-ло-ло!\nЯ водитель НЛО!')


def register_callback_handlers_change_ip(dp: Dispatcher):
    dp.register_callback_query_handler(change_ip, lambda c: c.data and c.data.startswith('change_ip'))
