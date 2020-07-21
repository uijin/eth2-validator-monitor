import configparser
import requests
import telegram
import time
import json
import logging
import atexit

# Load data from config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

validator_state = {
    'https://beaconcha.in/dashboard/data/validators?validators=31441': {
        'active': True
    },
    'https://altona.beaconcha.in/dashboard/data/validators?validators=4224': {
        'active': True
    }
}

@atexit.register
def say_goodbye():
    bot = telegram.Bot(token=config['TELEGRAM']['ACCESS_TOKEN'])
    bot.sendMessage(chat_id=config['CHAT']['ID'], text=f'Validator monitor leave, bye~')

if __name__ == '__main__':
    # print(config['TELEGRAM']['ACCESS_TOKEN'])
    bot = telegram.Bot(token=config['TELEGRAM']['ACCESS_TOKEN'])
    bot.sendMessage(chat_id=config['CHAT']['ID'], text=f"`Validator` monitor *start*\n```{json.dumps(validator_state, indent=2)}```", parse_mode='MarkdownV2')
    while True:
        for url in validator_state:
            res = requests.get(url)
            try:
                data = res.json()['data'][0]
            except json.decoder.JSONDecodeError as e:
                log.exception(res.text)
                continue
            log.info('%s, %s',data[1], data[3])
            index = data[1] # == k
            state = data[3]
            if (state == 'active_online') == validator_state[url]['active']:
                continue
            message = f'<b>{index}</b> change to {state}'
            message = message.replace('active_online', 'active_online👍')
            message = message.replace('active_offline', 'active_offline🗿')
            bot.send_message(chat_id=config['CHAT']['ID'], text=message, parse_mode='HTML')
            validator_state[url]['active'] = not validator_state[url]['active'] 
        time.sleep(5)

