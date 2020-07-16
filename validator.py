import configparser
import requests
import telegram
import time
import json

# Load data from config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

validator = {
    '31441': {
        'url': 'https://beaconcha.in/dashboard/data/validators?validators=31441',
        'active': True
    },
    '4224': {
        'url': 'https://altona.beaconcha.in/dashboard/data/validators?validators=4224',
        'active': True
    }
}

if __name__ == '__main__':
    # print(config['TELEGRAM']['ACCESS_TOKEN'])
    bot = telegram.Bot(token=config['TELEGRAM']['ACCESS_TOKEN'])
    bot.sendMessage(chat_id=config['CHAT']['ID'], text=f'Validator monitor start\n{json.dumps(validator, indent=2)}')
    while True:
        for k, v in validator.items():
            #print(k, v)
            res = requests.get(v['url'])
            data = res.json()['data'][0]
            print(data[1], data[3])
            index = data[1] # == k
            state = data[3]
            if (state == 'active_online') == validator[index]['active']:
                continue
            message = f'Validator {index} state change to {active}'
            bot.sendMessage(chat_id=config['CHAT']['ID'], text=message)
        time.sleep(3)

