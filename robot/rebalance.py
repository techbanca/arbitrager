def rebalance( currencies, polo ):
    for i in range(len(currencies)):
        while True:
            temp = polo.returnBalances()
            if(float(temp[currencies[i]]) > 0.009):
                # Push it to Bitcoin
                pair = 'BTC_' + currencies[i]
                v = float(temp[currencies[i]])
                while True:
                    try:
                        a = polo.sell(pair, BTC[i,0], v)
                        break
                    except:
                        BTC[i,0] = float(polo.returnOrderBook(currencyPair=pair, depth=1)['bids'][0][0])
            else:
                break
        while True:
            v = float(polo.returnBalances()['ETH'])
            if(float(temp['ETH']) > 0.0009):
                #v = float(temp['ETH'])
                while True:
                    try:
                        c = polo.sell('BTC_ETH', BTC_ETH_BID, v)
                        break
                    except Exception as e:
                        #print(e)
                        BTC_ETH_BID = float(polo.returnOrderBook(currencyPair='BTC_ETH', depth = 1)['bids'][0][0])
                        continue
            else:
                break
