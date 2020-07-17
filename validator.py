import configparser
import requests
import telegram
import time
import json
import logging

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

if __name__ == '__main__':
    # print(config['TELEGRAM']['ACCESS_TOKEN'])
    bot = telegram.Bot(token=config['TELEGRAM']['ACCESS_TOKEN'])
    bot.sendMessage(chat_id=config['CHAT']['ID'], text=f'Validator monitor start\n{json.dumps(validator, indent=2)}')
    while True:
        for url in validator_state:
            res = requests.get(url)
            try:
                data = res.json()['data'][0]
            except JSONDecodeError as e:
                log.exception(res.text)
                continue
            log.info('%s, %s',data[1], data[3])
            index = data[1] # == k
            state = data[3]
            if (state == 'active_online') == validator_state[url]['active']:
                continue
            message = f'Validator {index} state change to {state}'
            bot.sendMessage(chat_id=config['CHAT']['ID'], text=message)
            validator_state[url]['active'] = not validator_state[url]['active'] 
        time.sleep(3)

