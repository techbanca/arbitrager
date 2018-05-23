def getSpread(base_a, base_b, currencies, spread, depth, polo):
    base_pair = base_a + '_' + base_b
    temp = polo.returnOrderBook(depth=depth)
    spread[0][0] = temp[base_pair]['bids']
    spread[0][1] = temp[base_pair]['asks']
    for i in range(len(currencies)):
        f_pair = base_a + '_' + currencies[i]
        b_pair = base_b + '_' + currencies[i]
        spread[i+1] = [temp[f_pair]['bids'],temp[f_pair]['asks'],temp[b_pair]['bids'],temp[b_pair]['asks']] 
        #f_pair_bids = spread[f_pair]['bids']
        #f_pair_asks = spread[f_pair]['asks']
        #b_pair = base_b + '_' + currencies[i]
        #b_pair_bids = spread[b_pair]['bids']
        #b_pair_asks = spread[b_pair]['asks']
    return spread
