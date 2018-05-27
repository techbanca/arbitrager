import numpy as np
import pandas as pd
from poloniex import Poloniex, Coach

import polo_key
import getPairs
import createOrder
import rebalance
import getSpread

# Initialize the API
def initializePoloniex():
    key = polo_key.key()    
    secret = polo_key.secret()  
    myCoach = Coach()
    return Poloniex(key, secret, coach=myCoach)


def calculate_fees(fund_value, rate):
    temp = fund_value
    for i in range(3):
        temp = temp - (temp * rate)
    return fund_value - temp

def getFlow(spread, flow, fees):
    # flow[i,0] is ABC value / 1
    # flow[i,1] is ABC max Volume
    # flow[i,2] is CBA value / 1
    # flow[i,3] is CBA max Volume
    # Bid is 0
    # Ask is 1
    #abc = (fund_value / BTC[k,1] * ETH[k, 0] * BTC_ETH_BID) - taker_fees
    #cba = fund_value / BTC_ETH_ASK / ETH[k,1] * BTC[k,0] 
    for i in range(len(flow)):
        flow[i,0] = (1 / spread[i+1,1,0,0] * spread[i+1,2,0,0] * spread[0,0,0,0]) - fees
        flow[i,1] = (1 / spread[i+1,1,1,0] * spread[i+1,2,1,0] * spread[0,0,1,0]) - fees
        flow[i,2] = (1 / spread[0,1,0,0] / spread[i+1,3,0,0] * spread[i+1,0,0,0]) - fees
        flow[i,3] = (1 / spread[0,1,1,0] / spread[i+1,3,1,0] * spread[i+1,0,1,0]) - fees
        
        
    return flow

########### PARAMETERS ################
# Todo change this to the paramaters file
live = False
rebalance = True
exposure = 0.5
rate = 0.00
margin = 0.002
cutoff = 0.003
base_a = 'BTC'
base_b = 'ETH'
depth = 6

# Name our base_pair
#base_pair = base_a + '_' + base_b

# Initialize our mutual pairs for Trading
polo = initializePoloniex()
currencies = getPairs.getPairs(base_a, base_b, polo)  

# spread[[base,currency],[bid_a,ask_a,bid_b,ask_b],depth,[value, volume]]
spread = np.zeros([len(currencies)+1, 4, depth,2])
flow = np.zeros([len(currencies)-1,4])

print('Starting Trading... Live: ', live)
fund_value = float(polo.returnBalances()['BTC']) * exposure
print('Fund Value Exposed:', fund_value, ' BTC')

# Main Loop 
while True:
    if( live == True and rebalance == True):
        fund_value = rebalance.rebalance(currencies[i], polo)
        rebalance = False
    if(fund_value < cutoff):
        break
    
    fees = calculate_fees(fund_value, rate)
    
    # Get the Spread
    spread = getSpread.getSpread(base_a, base_b, currencies, spread, depth, polo) #polo.returnOrderBook()
    
    # Calculate the Flow
    flow = getFlow(spread, flow, fees)
    print(flow)

    
    '''
    # Get the ticker
    ticker = polo.returnTicker()
    BTC_ETH_BID = float(ticker['BTC_ETH']['highestBid']) 
    BTC_ETH_ASK = float(ticker['BTC_ETH']['lowestAsk']) 
    #print('ETH/BTC Bid: ', BTC_ETH_BID, '\tETH/BTC Ask: ',  BTC_ETH_ASK)
    for k in range(len(currencies)):
        btc_pair = 'BTC_' + currencies[k]
        eth_pair = 'ETH_' + currencies[k]
        BTC[k] = [float(ticker[btc_pair]['highestBid']),float(ticker[btc_pair]['lowestAsk'])]
        ETH[k] = [float(ticker[eth_pair]['highestBid']),float(ticker[eth_pair]['lowestAsk'])]
        abc = (fund_value / BTC[k,1] * ETH[k, 0] * BTC_ETH_BID) - taker_fees
        if( abc > fund_value + 0.0001):
            
            #Buy k/BTC Lowest Ask
            v = fund_value / BTC[k,1]
            #print('Buy ', currencies[k], ' from BTC')
            #print(v* BTC[k,1])
            #while True:
            try:
                a = polo.buy(btc_pair, BTC[k,1], v)
            except:
                break
            
            #Sell K/ETH Highest Bid
            v = v - (v*rate)
            #print('Sell ', currencies[k], ' for ETH')
            #print(v*ETH[k,0])
            while True:
                try:
                    b = polo.sell(eth_pair, ETH[k,0], v)
                    break
                except Exception as e:
                    print(e)
                    v = float(polo.returnBalances()[currencies[k]])
                    ETH[k,0] = float(polo.returnOrderBook(currencyPair=eth_pair, depth=1)['bids'][0][0])
                    continue
           
            #Sell ETH/BTC Highest Bid
            v = v * ETH[k,0]
            v = v - (v*rate)
            #print('Buy BTC from ETH')
            #print(v * BTC_ETH_BID)
            while True:
                try:
                    c = polo.sell('BTC_ETH', BTC_ETH_BID, v)
                    break
                except Exception as e:
                    print(e)
                    v = float(polo.returnBalances()['ETH'])
                    BTC_ETH_BID = float(polo.returnOrderBook(currencyPair='BTC_ETH', depth = 1)['bids'][0][0])
                    continue
            
            #print('Path Found BTC to ', currencies[k], ' to ETH to BTC')
            #fund_value = abc
            #print('Fund Value:', fund_value, ' BTC')
            rebalance = True
        cba = fund_value / BTC_ETH_ASK / ETH[k,1] * BTC[k,0] 
        if(cba > fund_value + 0.0001):
            
            # Buy ETH/BTC Lowest Ask
            v = fund_value / BTC_ETH_ASK
            #print('Buy ETH from BTC')
            #print(v * BTC_ETH_ASK)
            try:
                a = polo.buy('BTC_ETH', BTC_ETH_ASK, v)
             
            except:
                break
                
            # Buy K/ETH Lowest Ask
            v = v - (v*rate)
            v = v / ETH[k,1]
            #print('Buy ', currencies[k], ' from ETH')
            #print(v * ETH[k,1])
            while True:
                try:
                    b = polo.buy(eth_pair, ETH[k,1], v)
                    break
                except Exception as e:
                    #print(e)
                    #v = float(polo.returnBalances()[''])
                    ETH[k,1] = float(polo.returnOrderBook(currencyPair=eth_pair,depth=1)['asks'][0][0])
                    v = float(polo.returnBalances()['ETH']) / ETH[k,1]
                    continue
                
            # Sell K/BTC Highest Bid
            v = v - (v*rate)
            #print('Sell ', currencies[k], 'for BTC')
            #print(v * BTC[k,0])
            while True:
                try:
                    c = polo.sell(btc_pair, BTC[k,0], v)
                    break
                except Exception as e:
                    #print(e)
                    v = float(polo.returnBalances()[currencies[i]])
                    BTC[k,0] = float(polo.returnOrderBook(currencyPair=btc_pair, depth=1)['bids'][0][0])
                    continue
            
            rebalance = True
            #print('Path Found BTC to ETH to ', currencies[k],' to BTC')
            #fund_value = cba
            #print('Fund Value:', fund_value, ' BTC')
        #print('abc: ', abc, 'cba: ',  cba)
    '''
