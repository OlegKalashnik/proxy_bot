import json

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from parse import parser

parser.get_connection()
with open("devices.json", "r", encoding="utf-8") as f:
    servers = json.load(f)

servers_buttons = []
for space_server_name in servers:
    servers_buttons.append(
        InlineKeyboardButton(text=servers[space_server_name]['local_server_name'],
                             callback_data=f'server-{space_server_name}'))

inline_servers = InlineKeyboardMarkup(row_width=2)
inline_servers.add(*servers_buttons)
