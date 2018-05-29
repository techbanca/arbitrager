#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 15 15:44:05 2017
@author: garrettlee
@documentation: https://www.kraken.com/en-us/help/api#general-usage
"""

import requests

def getOrders(pair, depth):
    url = 'https://api.kraken.com/0/public/Depth?pair='+pair+'&count='+depth
    r = requests.get(url)
    return r.json()
    
def topAskBid(pair):
    orders = getOrders(pair, '1')['result'][pair]
    ask = float(orders['asks'][0][0])
    bid = float(orders['bids'][0][0])
    return ask, bid

def top5(pair):
    formattedAsks, formattedBids = [], []
    orders = getOrders(pair, '5')['result'][pair]
    asks, bids = orders['asks'], orders['bids']
    for ask in asks:
        formattedAsks.append((float(ask[0]), float(ask[1]), 'kraken'))
    for bid in bids:
        formattedBids.append((float(bid[0]), float(bid[1]), 'kraken'))
    return formattedAsks, formattedBids
