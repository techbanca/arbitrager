#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""

import requests

def getOrders(pair):
    r = requests.get('https://api.bitfinex.com/v1/book/'+pair)
    return r.json()

def topAskBid(pair):
    orders = getOrders(pair)
    ask = float(orders['asks'][0]['price'])
    bid = float(orders['bids'][0]['price'])
    return ask, bid
