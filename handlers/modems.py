from aiogram import types, Dispatcher
import json
from create_bot import bot

from parse import parser

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def show_modem(callback_query: types.CallbackQuery):
    with open('id.txt', 'r', encoding='utf-8') as f:
        auth_users = f.readlines()
    trusted = False
    for user in auth_users:
        if str(callback_query.from_user.id) == user.strip():
            trusted = True
            break

    if trusted:
        parser.get_connection()
        with open("devices.json", "r", encoding="utf-8") as f:
            servers = json.load(f)

        modem_buttons = []
        modem = servers[callback_query.data.split('-')[2]]['modems'][callback_query.data.split('-')[1]]
        modem_buttons.append(
            InlineKeyboardButton(text='Перезагрузить',
                                 callback_data=f'reboot_modem-{callback_query.data.split("-")[2]}-{callback_query.data.split("-")[1]}'))
        modem_buttons.append(
            InlineKeyboardButton(text='АВ тест', callback_data=f'check_modem-{callback_query.data.split("-")[2]}-{callback_query.data.split("-")[1]}'))
        if modem["change_ip"]:
            modem_buttons.append(
                InlineKeyboardButton(text='Сменить ай-пи', callback_data=f'change_ip-{callback_query.data.split("-")[2]}-{callback_query.data.split("-")[1]}'))

        inline_modem = InlineKeyboardMarkup(row_width=2)
        inline_modem.add(*modem_buttons)

        servers_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        bts_button = KeyboardButton('/Servers')
        servers_kb.add(bts_button)

        message_text = f'{callback_query.data.split("-")[1]}\n'
        message_text += 'Продаётся\n' if modem["for_sell"] else 'Не продаётся\n'
        message_text += 'Продан\n' if modem["status"] == 'sold' else 'Не продан\n'

        await bot.send_message(
            callback_query.from_user.id,
            text=message_text,
            reply_markup=inline_modem)
        await bot.send_message(
            callback_query.from_user.id,
            text='Смотри не сломай!',
            reply_markup=servers_kb)
    else:
        await callback_query.answer('Тыщь пыщь тро-ло-ло!\nЯ водитель НЛО!')


def register_callback_handlers_modems(dp: Dispatcher):
    dp.register_callback_query_handler(show_modem, lambda c: c.data and c.data.startswith('modem'))
