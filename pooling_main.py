from aiogram.utils import executor
from create_bot import dp
from parse import parser

from handlers import start
from handlers import servers
from handlers import modems
from handlers import space
from handlers import change_ip
from handlers import check_modem
from handlers import reboot_modem
from handlers import reboot_3proxy


start.register_message_handlers_start(dp)
servers.register_callback_handlers_servers(dp)
modems.register_callback_handlers_modems(dp)
check_modem.register_callback_handlers_check_modem(dp)
reboot_modem.register_callback_handlers_reboot_modem(dp)
space.register_message_handlers_space(dp)
change_ip.register_callback_handlers_change_ip(dp)
reboot_3proxy.register_callback_handlers_reboot_3proxy(dp)

parser.run()
executor.start_polling(dispatcher=dp, skip_updates=True)
