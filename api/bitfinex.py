#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""

import requests

def getOrders(pair):
    r = requests.get('https://api.bitfinex.com/v1/book/'+pair)
    return r.json()

