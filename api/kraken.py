#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

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
    orders = getOrders(pair, '6')['result'][pair]
    asks, bids = orders['asks'], orders['bids']
    for ask in asks:
        formattedAsks.append((float(ask[0]), float(ask[1]), 'kraken'))
    for bid in bids:
        formattedBids.append((float(bid[0]), float(bid[1]), 'kraken'))
    return formattedAsks, formattedBids

"""#x = requests.get('https://api.kraken.com/0/public/AssetPairs').json()['result']
xkeys = ['DASHEUR', 'DASHUSD', 'DASHXBT', 'EOSETH', 'EOSEUR', 'EOSUSD', 'EOSXBT', 'GNOETH', 'GNOEUR', 'GNOUSD', 'GNOXBT', 'USDTZUSD', 'XETCXETH', 'XETCXXBT', 'XETCZEUR', 'XETCZUSD', 'XETHXXBT', 'XETHXXBT.d', 'XETHZCAD', 'XETHZCAD.d', 'XETHZEUR', 'XETHZEUR.d', 'XETHZGBP', 'XETHZGBP.d', 'XETHZJPY', 'XETHZJPY.d', 'XETHZUSD', 'XETHZUSD.d', 'XICNXETH', 'XICNXXBT', 'XLTCXXBT', 'XLTCZEUR', 'XLTCZUSD', 'XMLNXETH', 'XMLNXXBT', 'XREPXETH', 'XREPXXBT', 'XREPZEUR', 'XREPZUSD', 'XXBTZCAD', 'XXBTZCAD.d', 'XXBTZEUR', 'XXBTZEUR.d', 'XXBTZGBP', 'XXBTZGBP.d', 'XXBTZJPY', 'XXBTZJPY.d', 'XXBTZUSD', 'XXBTZUSD.d', 'XXDGXXBT', 'XXLMXXBT', 'XXLMZEUR', 'XXLMZUSD', 'XXMRXXBT', 'XXMRZEUR', 'XXMRZUSD', 'XXRPXXBT', 'XXRPZCAD', 'XXRPZEUR', 'XXRPZJPY', 'XXRPZUSD', 'XZECXXBT', 'XZECZEUR', 'XZECZUSD']
y=requests.get('https://api.kraken.com/0/public/Assets').json()"""
