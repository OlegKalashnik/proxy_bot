import json
import time

from bs4 import BeautifulSoup as bs
import requests


class Client:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.60 YaBrowser/20.12.0.966 Yowser/2.5 Safari/537.36'
        }
        self.URL = 'https://mobileproxy.space'
        self.devices = {}
        self.last_connection = 0
        self.ready_dict = False

    def get_connection(self):
        time_delta = time.time() - self.last_connection
        if self.last_connection == 0 or time_delta > 300:
            try:
                self.last_connection = time.time()
                r = self.session.get(self.URL, verify=False)
                soup = bs(r.text, 'html.parser')
                token = soup.select('[name="CRFXTOKEN"]')
                if (len(token) > 0):
                    token = token[0]['value']

                    params = {
                        'phone': u'userphone',
                        'password': u'userpassword',
                        'CRFXTOKEN': token
                    }
                    r = self.session.post(self.URL, params)
                self.parse_servers()
            except Exception as e:
                print(f'get_connection {e}')

    def parse_servers(self):
        try:
            r = self.session.get('https://mobileproxy.space/user.html?modems&load_modems=1')
            soup = bs(r.text, 'html.parser')
            self.modems_to_dict(soup, 'tr.table-success', 'sold')
            self.modems_to_dict(soup, 'tr.table-warning', 'not_sold')
        except:
            pass

        try:
            r = self.session.get('https://mobileproxy.space/user.html?modems&load_servers=1')
            soup = bs(r.text, 'html.parser')
            self.servers_to_dict(soup.find('tbody'))
        except:
            pass
        # Serializing json
        json_object = json.dumps(self.devices, indent=4, ensure_ascii=False)

        # Writing to devices.json
        with open("devices.json", "w", encoding="utf-8") as outfile:
            outfile.write(json_object)
        self.ready_dict = True

    def modems_to_dict(self, soup, selector, modem_status):
        trs = soup.select(selector)
        for tr in trs:
            soup = bs(str(tr), 'html.parser')
            checked = soup.select('input.phone_list_canbuy')
            if str(checked).find('checked') > 0:
                for_sell = True
            else:
                for_sell = False

            change_ip = ''
            reboot_link = ''
            for a in soup.select('a.dropdown-item'):
                if a.string == 'Перезагрузить модем':
                    reboot_link = a['href']
                    break
            if modem_status == 'not_sold':
                for a in soup.select('a.dropdown-item'):
                    if a.string == 'Сменить IP':
                        change_ip = a['href']
                        break
            check_modem_link = soup.find('a', {"title": "Проверить работоспособность прокси"})['href']
            tds = soup.findAll('td')
            try:
                space_server_name = str(tds[-1]).split(' ')[-1][1:-6]
                try:
                    self.devices[space_server_name]['local_server_name'] = '.'.join(tds[3].string.split('.')[1:])
                except:
                    self.devices[space_server_name] = {}
                    self.devices[space_server_name]['local_server_name'] = '.'.join(tds[3].string.split('.')[1:])
                try:
                    self.devices[space_server_name]['modems'][tds[3].string] = {}
                except:
                    self.devices[space_server_name]['modems'] = {}
                    self.devices[space_server_name]['modems'][tds[3].string] = {}

                self.devices[space_server_name]['modems'][tds[3].string]['status'] = modem_status
                self.devices[space_server_name]['modems'][tds[3].string]['for_sell'] = for_sell
                self.devices[space_server_name]['modems'][tds[3].string]['reboot_link'] = reboot_link
                self.devices[space_server_name]['modems'][tds[3].string]['change_ip'] = change_ip
                self.devices[space_server_name]['modems'][tds[3].string]['check_modem_link'] = check_modem_link

            except:
                pass

    def servers_to_dict(self, soup):
        space_server_name = ''
        trs = soup.select('tr')
        for tr in trs:
            soup = bs(str(tr), 'html.parser')
            tds = soup.findAll('td')
            try:
                try:
                    space_server_name = str(tds[2].text.split())[2: -2].split(' ')[1][1:]
                except:
                    space_server_name = str(tds[2].text.split())[2: -2]
                reboot_3proxy_link = soup.find('a', {"title": "Reboot 3proxy"})['href']
                self.devices[space_server_name]['reboot_3proxy_link'] = reboot_3proxy_link
            except Exception as e:
                print(f'servers_to_dict {e}')

    def reboot_modem(self, server, modem):
        try:
            last_action = 0
            try:
                last_action = self.devices[server]["modems"][modem]["last_reboot_modem"]
            except:
                pass
            if last_action == 0 or time.time() - last_action > 300:
                link = self.devices[server]["modems"][modem]["reboot_link"]
                self.devices[server]["modems"][modem]["last_reboot_modem"] = time.time()
                r = self.session.get(f'https://mobileproxy.space{link}').text
                if r:
                    return r
                else:
                    return 'Сервер не ответил'
            else:
                return f'Перезагружал {modem} менее 5-ти минут назад'
        except:
            return 'Не могу получить ссылку, попробуй через 5 минут'

    def change_ip(self, server, modem):
        try:
            link = self.devices[server]["modems"][modem]["change_ip"]
            r = self.session.get(f'https://mobileproxy.space{link}').text
            if r:
                return r
            else:
                return 'Сервер не ответил'
        except:
            return 'Не могу получить ссылку, попробуй через 5 минут'

    def check_modem(self, server, modem):
        try:
            link = self.devices[server]["modems"][modem]["check_modem_link"]
            r = self.session.get(f'https://mobileproxy.space{link}').text
            if r:
                return r
            else:
                return 'Сервер не ответил'
        except:
            return 'Не могу получить ссылку, попробуй через 5 минут'

    def reboot_3proxy(self, server):
        last_action = 0
        try:
            last_action = self.devices[server]["last_reboot_3proxy"]
        except:
            pass
        if last_action == 0 or time.time() - last_action > 300:
            try:
                link = self.devices[server]["reboot_3proxy_link"]
                self.devices[server]["last_reboot_3proxy"] = time.time()
                r = self.session.get(f'https://mobileproxy.space{link}').text
                if r:
                    return r
                else:
                    return 'Сервер не ответил'
            except:
                return 'Не могу получить ссылку, попробуй через 5 минут'
        else:
            return 'Перезагружал 3proxy менее 5-ти минут назад'

    def run(self):
        self.get_connection()

parser = Client()
# if __name__ == "__main__":
#     parser = Client()
#
#     parser.get_connection()