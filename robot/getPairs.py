def getPairs(base_a, base_b, polo):
    # Get all the active Currencies
    temp = polo.returnCurrencies()
    currencies = []
    for key in temp.items():
        if((key[1]['delisted'] == 0) and (key[0] != (base_a or base_b))):
            currencies.append(key[0])
    
    # Initialize Dataframe    
    #BTC, ETH, XMR, USDT = np.zeros([len(currencies),2]), np.zeros([len(currencies),2]),np.zeros([len(currencies),2]), np.zeros([len(currencies),2])
    
    remove = list()
    ticker = polo.returnTicker()
    #BTC_ETH_BID = ticker['BTC_ETH']['highestBid'] 
    #BTC_ETH_ASK = ticker['BTC_ETH']['lowestAsk']
    for i in range(len(currencies)):
        pair = base_a + '_' + currencies[i]
        pair_b = base_b + '_' + currencies[i]
        try:
            A = ticker[pair]['highestBid']
            B = ticker[pair_b]['highestBid']
            print('Valid Chain: ', pair, ' and ', pair_b)
        except:
            #print(e)
            remove.append(currencies[i]) # Flag for Removal
    
    for j in range(len(remove)):
        currencies.remove(remove[j])
    
    return currencies
