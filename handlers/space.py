from aiogram import types, Dispatcher

from parse import parser


async def space_notify(message: types.Message):
    with open('id.txt', 'r', encoding='utf-8') as f:
        auth_users = f.readlines()
    trusted = False
    for user in auth_users:
        if str(message.from_user.id) == user.strip():
            trusted = True
            break

    if trusted:
        parser.get_connection()
        errors_list = message.text.split('\n')
        for error in errors_list[1:]:
            if error.split(' ')[1] == 'беда':
                server = str(error.split('(')[0])
                await message.answer(f'Перезагружаю 3proxy {server} ...')
                await message.answer(f'{server}\n{parser.reboot_3proxy(server)}')
                continue
            if error.split(' ')[1].split('.')[2] == 'space':
                server = str(error.split(' ')[1])
                modem = error.split(' ')[2][0: -1]
                await message.answer(f'Перезагружаю модем {modem} ...')
                await message.answer(f'{server} {modem}\n{parser.reboot_modem(server, modem)}')
    else:
        await message.answer('Тыщь пыщь тро-ло-ло!\nЯ водитель НЛО!')


def register_message_handlers_space(dp: Dispatcher):
    dp.register_message_handler(space_notify, lambda c: c.text and c.text.startswith('🕸 Mobileproxy.space:'))
