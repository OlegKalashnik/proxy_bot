from aiogram import types, Dispatcher
import json
from create_bot import bot

from parse import parser

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def show_modems(callback_query: types.CallbackQuery):
    parser.get_connection()
    with open('id.txt', 'r', encoding='utf-8') as f:
        auth_users = f.readlines()
    trusted = False
    for user in auth_users:
        if str(callback_query.from_user.id) == user.strip():
            trusted = True
            break

    if trusted:

        with open("devices.json", "r", encoding="utf-8") as f:
            servers = json.load(f)

        modems_buttons = []
        modems = servers[callback_query.data.split('-')[1]]['modems']
        for modem in modems:
            modems_buttons.append(
                InlineKeyboardButton(text=modem,
                                     callback_data=f'modem-{modem}-{callback_query.data.split("-")[1]}'))

        inline_modems = InlineKeyboardMarkup(row_width=2)
        inline_modems.add(*modems_buttons)

        inline_server = InlineKeyboardMarkup(row_width=2)
        r_3proxy = InlineKeyboardButton(text='Reboot 3proxy',
                                        callback_data=f'reboot_3proxy-{callback_query.data.split("-")[1]}')
        r_server = InlineKeyboardButton(text='Reboot server',
                                        callback_data=f'r_server-{callback_query.data.split("-")[1]}')
        inline_server.add(r_server, r_3proxy)

        servers_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        bts_button = KeyboardButton('/Servers')
        servers_kb.add(bts_button)

        await bot.send_message(
            callback_query.from_user.id,
            text=callback_query.data.split('-')[1],
            reply_markup=inline_server)
        await bot.send_message(
            callback_query.from_user.id,
            text=callback_query.data.split('-')[1],
            reply_markup=inline_modems)
        await bot.send_message(
            callback_query.from_user.id,
            text='Выберите модем',
            reply_markup=servers_kb)
    else:
        await callback_query.answer('Тыщь пыщь тро-ло-ло!\nЯ водитель НЛО!')


def register_callback_handlers_servers(dp: Dispatcher):
    dp.register_callback_query_handler(show_modems, lambda c: c.data and c.data.startswith('server'))
