
from api_wrappers import CryptoMKT, SurBTC, Pushbullet

import time

import vars





def check_price_differences(threshold, check_delay):

    pushbullet = Pushbullet(vars.pushbullet_token)

    while True:

        cryptomkt_prices = CryptoMKT.get_prices()

        surbtc_prices = SurBTC.get_prices()



        print(cryptomkt_prices)

        print(surbtc_prices)



        if cryptomkt_prices['bid'] - surbtc_prices['ask'] >= threshold:

            title = 'Arbitrage oportunity!'

            body = ('CryptoMKT\'s bid is {}CLP greater than SurBTC\'s ask.'

                    .format(cryptomkt_prices['bid'] - surbtc_prices['ask']))

            pushbullet.push_note(title, body)

            print(body)

        elif surbtc_prices['bid'] - cryptomkt_prices['ask'] >= threshold:

            title = 'Arbitrage oportunity!'

            body = ('SurBTC\'s bid is {}CLP greater than CryptoMKT\'s ask.'

                    .format(surbtc_prices['bid'] - cryptomkt_prices['ask']))

            pushbullet.push_note(title, body)

            print(body)

        time.sleep(check_delay)
