#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

def getOrders(pair):
    r = requests.get('https://cryptottlivewebapi.xbtce.net:8443/api/v1/public/ticker/'+pair)
    return r.json()

def topAskBid(pair):
    orders = getOrders(pair)
    ask = float(orders[0]['BestAsk'])
    bid = float(orders[0]['BestBid'])
    return ask, bid
        
a = {'dash-bitcoin':'DSHBTC','emercoin-bitcoin':'EMCBTC',
'ethereum-bitcoin':'ETHBTC','litecoin-ethereum':'ETHLTC',
'litecoin-bitcoin':'LTCBTC','namecoin-bitcoin':'NMCBTC',
'peercoin-bitcoin':'PPCBTC'}


"""r = requests.get('https://cryptottlivewebapi.xbtce.net:8443/api/v1/public/symbol').json()
for thing in r:
    d = thing['Description']
    if d in a:
        print(thing['Symbol'])
 """  
