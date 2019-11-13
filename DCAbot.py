from getpass import getpass
from pprint import pprint
import requests
import time
import json
import hashlib
import hmac
import sys

class DCAbot:

    def __init__(self):
        self.api_key = 'PUT YOUR API KEY HERE (NOT SECRET KEY)'
        
    def read_secret(self):
        # Let's be secure. Just make sure you don't have a keylogger.
        # Do not type your secret key into this file: this script will ask for input when you run it.
        self.api_secret = getpass(prompt='API secret: ')

    def parse_interval(self, x):
        if x == "w":
            return 604800
        elif x == "d":
            return 86400
        elif x == "h":
            return 3600
        elif x == "m":
            return 60
        elif x == "s":
            return 1
        else:
            print("Invalid input. Enter number + w, d, h, m or s. Example = 1w, 4d, 11h, 20m or 30s") 
            sys.exit()

    def read_purchase_interval(self):
        i = input('How much time should the bot wait between buying? (1d, 3h, 20m, etc) : ')
        self.purchase_interval = int(i[:-1]) * self.parse_interval(i[-1])
        print(self.purchase_interval)

    def read_purchase_volume(self):
        # TODO: Make this work
        self.purchase_volume = input('Spend how much JPY each purchase? (orders below 0.001BTC will fail)')

    def sleep(self):
        time.sleep(float(self.purchase_interval) - (time.time() % float(self.purchase_interval)))

    def run(self):
        while True:
            domain = "https://api.bitflyer.com"

            # Get the latest price for analysis later
            path = "/v1/getticker"
            response = requests.get(domain + path)
            data = response.json()
            current_price = data['ltp']

            # Make an order
            path = "/v1/me/sendchildorder"
            method = "POST"
            order_info = {
                    "product_code": "BTC_JPY",
                    "child_order_type": "MARKET",
                    "side": "BUY",
                    "size": 0.001 #float(self.purchase_volume) / current_price
            }
            body = json.dumps(order_info)

            timestamp = str(time.time())
            text = str.encode(timestamp + method + path + body)
            encoded_key = str.encode(self.api_secret)
            sign = hmac.new(encoded_key, text, hashlib.sha256).hexdigest()

            header = {
                "ACCESS-KEY": self.api_key,
                "ACCESS-TIMESTAMP": timestamp,
                "ACCESS-SIGN": sign,
                "Content-Type": "application/json"
            }

            options = {
                "url": domain + path,
                "method": method,
                "body": body,
                "headers": header
            }


            try:
                with requests.Session() as sess:
                    if header:
                        sess.headers.update(header)
 
                    response = sess.post(domain + path, data=json.dumps(order_info), timeout=500)

            except requests.RequestException as ex:
                print(ex)
                raise ex

            if len(response.content) > 0:
                print(json.loads(response.content.decode("utf-8")))

            self.sleep()

if __name__ == '__main__':
    bot = DCAbot()

    bot.read_secret()
    bot.read_purchase_interval()
    bot.read_purchase_volume()

    bot.run()
