from getpass import getpass
from pprint import pprint
import requests
import time
import json

class DCAbot:

    def __init__(self):
        self.api_key = 'PUT YOUR API KEY HERE (NOT SECRET KEY)'
        
    def read_secret(self):
        self.api_secret = getpass(prompt='API secret:')

    def read_purchase_interval(self):
        self.purchase_interval = input('How often do you want to buy bitcoin? (in seconds) ')

    def read_purchase_volume(self):
        self.purchase_volume = input('How much JPY will you spend every ' \
                                    + self.purchase_interval + ' seconds? ')

    def sleep(self):
        time.sleep(float(self.purchase_interval) - (time.time() % float(self.purchase_interval)))

    def run(self):
        while True:
            response = requests.get('https://api.bitflyer.com/v1/getticker')
            data = response.json()
            current_price = data['ltp']

            #response = requests.post('https://api.bitflyer.com/v1/me/sendchildorder')
            product_code = "BTC_JPY"
            child_order_type = "MARKET"
            side = "BUY"
            size = float(self.purchase_volume) / current_price
            print(size)

            body = product_code + child_order_type + side + str(size)
            pprint(json.dumps(body))

            #timestamp = data['timestamp']
            #print('Buying ' + self.purchase_volume + ' @ ' + str(current_price) + ' @ ' + str(time.time()))
            self.sleep()

if __name__ == '__main__':
    bot = DCAbot()

    bot.read_secret()
    bot.read_purchase_interval()
    bot.read_purchase_volume()

    bot.run()
