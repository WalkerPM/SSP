#!/bin/python3
import yaml
import requests
import logging
from time import sleep
from os import environ
from telegram_text import PlainText
from dotenv import load_dotenv

load_dotenv()

CHAT_ID = environ.get("CHAT_ID")
BOT_TOKEN = environ.get("BOT_TOKEN")

CONFIG_FILENAME = "service-list.yaml"

logging.basicConfig(
    level=logging.INFO, format="[%(asctime)s: %(levelname)s] %(message)s"
)




class Service:
    def __init__(self, name, address, protocol, port: str = "0000", route: str = "/") -> None:
        self.name: str = name
        self.address: str = address
        self.protocol: str = protocol
        self.port: str = port
        self.route: str = route
        self.status: bool = True
        self.notified: bool = False
        self.retries: int = 2
        pass

    def change_status(self):
        if (self.status):
            self.status = False
        else:
            self.status = True

    def check_http(self, secure: bool = False):
        failed_tries = 0

        for i in range(self.retries):
            try:
                if secure:
                    check_request = requests.get(f'https://{self.address}:{self.port}{self.route}', timeout=10)
                else:
                    check_request = requests.get(f'http://{self.address}:{self.port}{self.route}', timeout=10)
            except Exception as e:
                logging.error(e)
                failed_tries += 1
        
        if failed_tries == self.retries:
            return False

        if check_request.status_code < 400:
            return True
        else:
            return False

    def check_state(self):
        match self.protocol:
            case "http":
                return self.check_http()
            case "https":
                return self.check_http(secure=True)
            case _ :
                return True

    def __repr__(self):
        return (f'Service name: {self.name} \n' +
                f'Service address: {self.address} \n' +
                f'Service protocol: {self.protocol} \n'+
                f'Service port: {self.port}')
    
def send_msg(current_service: Service, 
             status="Dead"):
    
    send_msg = str(current_service) + f"\nStatus: {status}"

    send_text = f'{PlainText(send_msg).to_markdown()}'

    send_data = {"chat_id": CHAT_ID ,
             "parse_mode": "MarkdownV2",
             "text": send_text
             }
    
    send_url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    
    try:
        sended_request = requests.post(url=send_url, data=send_data)
        sended_request.raise_for_status()
    except Exception as e:
        logging.warning("Exception in sending process.")
        logging.exception(e)
    finally:
        if isinstance(sended_request, requests.Response):
            logging.info(f"Status of message: {sended_request.status_code}")
        logging.info(send_msg)
    pass

def check_availability(services: list):
    for i in services:
            if not i.check_state():
                logging.warning(f'{i.name} is not available!')
                if i.status == 0:
                    pass
                else:
                    i.change_status()
            else:
                if i.status == False:
                    i.change_status()
                    i.notified = False
                    send_msg(i, "is up! ✅")
                logging.info(f'{i.name} is available') 
        
    all = len(services)
    available = 0
    unavailable = 0

    for i in services:
        
        if i.status == 1:
            available += 1
        else:
            unavailable += 1

        if i.status == 0 and i.notified == False:
            send_msg(i, "is DOWN! ❌")
            i.notified = True

    logging.info(f'Total hosts: {all}. Available : {available}. Unavailable: {unavailable}.')

if __name__ == "__main__":

    logging.warning("Application started!")

    services = []

    with open(CONFIG_FILENAME,'r+',encoding='utf-8') as f:
        list_of_services = yaml.safe_load(f.read())
    
    for i in list_of_services:
        
        curr_service = Service(name = i['name'],
                                address = i['address'],
                                protocol = i['protocol'])
        if 'port' in i:
            curr_service.port = i['port']
        
        if 'route' in i: 
            curr_service.route = i['route']
    
        services.append(curr_service)

    while(True):
        check_availability(services)
        sleep(120)
