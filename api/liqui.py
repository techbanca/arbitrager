#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

liquiPairs = {'litecoin-tether': 'ltc_usdt', 'bitcoin-tether': 'btc_usdt', 'dash-tether': 'dash_usdt', 'ethereum-tether': 'eth_usdt', 'iconomi-tether': 'icn_usdt', 'golem-tether': 'gnt_usdt', 'waves-tether': 'waves_usdt', 'gnosis-tether': 'gno_usdt'}

def getOrders(pair):
    r = requests.get('https://api.liqui.io/api/3/depth/'+pair)
    return r.json()

def topAskBid(pair):
    orders = getOrders(pair)[pair]
    ask = float(orders['asks'][0][0])
    bid = float(orders['bids'][0][0])
    return ask, bid
    
    
