# coding=utf-8
from __future__ import print_function, absolute_import, unicode_literals
from gm.api import *
import numpy as np
def init(context):
    context.goods = ['SHFE.rb1801', 'SHFE.hc1801']
    subscribe(symbols=context.goods, frequency='60s', count=31, wait_group=True)
def on_bar(context, bars):
    data_rb = context.data(symbol=context.goods[0], frequency='60s', count=31, fields='close')
    close_rb = data_rb.values
    data_hc = context.data(symbol=context.goods[1], frequency='60s', count=31, fields='close')
    close_hc = data_hc.values
    spread = close_rb[:-1] - close_hc[:-1]
    up = np.mean(spread) + 2 * np.std(spread)
    down = np.mean(spread) - 2 * np.std(spread)
    spread_now = close_rb[-1] - close_hc[-1]
    position_rb_long = context.account().position(symbol=context.goods[0], side=PositionSide_Long)
    position_rb_short = context.account().position(symbol=context.goods[0], side=PositionSide_Short)
    if not position_rb_long and not position_rb_short:
        if spread_now > up:
            order_target_volume(symbol=context.goods[0], volume=1, order_type=OrderType_Market,
                                position_side=PositionSide_Short)
            print(context.goods[0], 'once')
            order_target_volume(symbol=context.goods[1], volume=1, order_type=OrderType_Market,
                                position_side=PositionSide_Long)
            print(context.goods[1], 'more')
        if spread_now < down:
            order_target_volume(symbol=context.goods[0], volume=1, order_type=OrderType_Market,
                                position_side=PositionSide_Long)
            print(context.goods[0], 'more')
            order_target_volume(symbol=context.goods[1], volume=1, order_type=OrderType_Market,
                                position_side=PositionSide_Short)
            print(context.goods[1], 'once')
    elif position_rb_short:
        if spread_now <= up:
            order_close_all()
            print('regression')
        if spread_now < down:
            order_target_volume(symbol=context.goods[0], volume=1, order_type=OrderType_Market,
                                position_side=PositionSide_Long)
            print(context.goods[0], 'onec')
            order_target_volume(symbol=context.goods[1], volume=1, order_type=OrderType_Market,
                                position_side=PositionSide_Short)
            print(context.goods[1], 'asdfg')
    elif position_rb_long:
        if spread_now >= down:
            order_close_all()
        if spread_now > up:
            order_target_volume(symbol=context.goods[0], volume=1, order_type=OrderType_Market,
                                position_side=PositionSide_Short)
            print(context.goods[0], 'ik')
            order_target_volume(symbol=context.goods[1], volume=1, order_type=OrderType_Market,
                                position_side=PositionSide_Long)
            print(context.goods[1], 'jj')
if __name__ == '__main__':

    run(strategy_id='strategy_id',
        filename='main.py',
        mode=MODE_BACKTEST,
        token='token_id',
        backtest_start_time='2018-01-01 08:00:00',
        backtest_end_time='2018-01-01 16:00:00',
        backtest_adjust=ADJUST_PREV,
        backtest_initial_cash=500000,
        backtest_commission_ratio=0.0001,
        backtest_slippage_ratio=0.0001)
