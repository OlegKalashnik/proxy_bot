import ssl
import time

from aiohttp import web


from aiogram.dispatcher.webhook import get_new_configured_app

from parse import parser

from create_bot import dp, bot

from handlers import start
from handlers import servers
from handlers import modems
from handlers import space
from handlers import change_ip
from handlers import check_modem
from handlers import reboot_modem
from handlers import reboot_3proxy



WEBHOOK_HOST = 'Domain name or IP address which your bot is located'  # Domain name or IP address which your bot is located.
WEBHOOK_PORT = 8443  # Telegram Bot API allows only for usage next ports: 443, 80, 88 or 8443
WEBHOOK_URL_PATH = '/webhook'  # Part of URL

# These options needed if you use self-signed SSL certificate
# Instructions: https://core.telegram.org/bots/self-signed
WEBHOOK_SSL_CERT = 'C:/proxy_bot/public.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = 'C:/proxy_bot/private.key'  # Path to the ssl private key

WEBHOOK_URL = f"https://{WEBHOOK_HOST}:{WEBHOOK_PORT}{WEBHOOK_URL_PATH}"

# Web app settings:
#   Use LAN address to listen webhooks
#   User any available port in range from 1024 to 49151 if you're using proxy, or WEBHOOK_PORT if you're using direct webhook handling
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = 8443


# async def cmd_start(message: types.Message):
#     # Yep. aiogram allows to respond into webhook.
#     # https://core.telegram.org/bots/api#making-requests-when-getting-updates
#     return SendMessage(chat_id=message.chat.id, text='Hi from webhook!',
#                        reply_to_message_id=message.message_id)


async def on_startup(app):
    # Demonstrate one of the available methods for registering handlers
    # This command available only in main state (state=None)
    # dp.register_message_handler(cmd_start, commands=['start'])
    start.register_message_handlers_start(dp)
    servers.register_callback_handlers_servers(dp)
    modems.register_callback_handlers_modems(dp)
    check_modem.register_callback_handlers_check_modem(dp)
    reboot_modem.register_callback_handlers_reboot_modem(dp)
    space.register_message_handlers_space(dp)
    change_ip.register_callback_handlers_change_ip(dp)
    reboot_3proxy.register_callback_handlers_reboot_3proxy(dp)

    # Get current webhook status
    webhook = await bot.get_webhook_info()
    # If URL is bad
    if webhook.url != WEBHOOK_URL:
        # If URL doesn't match current - remove webhook
        if not webhook.url:
            await bot.delete_webhook()

        # Set new URL for webhook
        await bot.set_webhook(WEBHOOK_URL, certificate=open(WEBHOOK_SSL_CERT, 'rb'))
        # If you want to use free certificate signed by LetsEncrypt you need to set only URL without sending certificate.


async def on_shutdown(app):
    """
    Graceful shutdown. This method is recommended by aiohttp docs.
    """
    # Remove webhook.
    await bot.delete_webhook()

    # Close Redis connection.
    await dp.storage.close()
    await dp.storage.wait_closed()


if __name__ == '__main__':
    while True:
        time.sleep(5)
        if parser.ready_dict:
            # Get instance of :class:`aiohttp.web.Application` with configured router.
            app = get_new_configured_app(dispatcher=dp, path=WEBHOOK_URL_PATH)

            # Setup event handlers.
            app.on_startup.append(on_startup)
            app.on_shutdown.append(on_shutdown)

            # Generate SSL context
            context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            context.load_cert_chain(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV)

            # Start web-application.
            web.run_app(app, host=WEBAPP_HOST, port=WEBAPP_PORT, ssl_context=context)
            # Note:
            #   If you start your bot using nginx or Apache web server, SSL context is not required.
            #   Otherwise, you need to set `ssl_context` parameter.
            break
