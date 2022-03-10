
from collections import deque
import logging

import pandas as pd
from alg_modules.alg_handler import AlgHandler

from paper_trade import PaperTrader
from stop_loss import StopLoss


class TradeStrategy(object): 
    # TODO refactor later
    # '''docstring for TradeStrategy'''
    # def __init__(self, ):
    #     super(TradeStrategy, self).__init__()
        
    @staticmethod
    def trade_strategy(**kwargs):
        STOP_LOSS_ENABLED = kwargs.get('STOP_LOSS_ENABLED', False)
        STOP_LOSS_THRESHOLD = kwargs.get('STOP_LOSS_THRESHOLD', 0)
        stop_loss_trade_flag = kwargs.get('stop_loss_trade_flag', 0)
        df = kwargs.get('df', None) 
        # global stop_loss_trade_flag
        stop_loss_trade_flag = False
        MA_list = (2, 25, 100, 200)

        window = deque(maxlen=200)
        p_trdr = PaperTrader(
            main_currency_label='RVN',
            secondary_currency_label='USD',
            main_currency_amount=100,
            secondary_currency_amount=0,
            fee=0.1,
        )
        # create empty dataframe w/ columns from p_trdr
        trade_data = pd.DataFrame(
            columns = p_trdr.get_df(timestamp=df.iloc[-1]['date_created']).columns.values
        )
        trade_data['reason'] = ''
        stop_loss = StopLoss(
            STOP_LOSS_THRESHOLD=STOP_LOSS_THRESHOLD,
        )
        # init alg
        alg = AlgHandler(
            df=pd.DataFrame([]),
            MA_list=MA_list,
            )
        for _, row in df.iterrows():
            window.append(dict(row))
            df_ = pd.DataFrame(window)
            alg.update_data(df_)
            alg.calculate(val_col='open_', time_col='open_time',)
            do_trade, cross_type = alg.evaluate()
            # if stop_loss_trade_flag: logging.info(f'holy {stop_loss_trade_flag}')
            if STOP_LOSS_ENABLED:
                stop_loss_trade_flag, trade_data = stop_loss.stop_loss_alg(
                    stop_loss_trade_flag=stop_loss_trade_flag,
                    trade_data=trade_data,
                    p_trdr=p_trdr,
                    row=row,
                )
            # if stop_loss_trade_flag: logging.info(f'pog {stop_loss_trade_flag}')
            ## do not allow same operation twise in a row
            if do_trade :
                # logging.info(f'pepe {stop_loss_trade_flag}')
                trade_data, stop_loss_trade_flag = TradeStrategy.trade_alg(stop_loss_trade_flag, trade_data, p_trdr, row, cross_type)
                # print(stop_loss_trade_flag)
        return stop_loss.stop_loss_count, trade_data, p_trdr

    @staticmethod
    def trade_alg(stop_loss_trade_flag_, trade_data, p_trdr, row, cross_type):
        trade_type = "SELL" if cross_type=='raise' else "BUY"
        # do not SELL on first trade
        if  (len(trade_data) > 0) or (trade_type == "BUY"):
            # logging.info(f'{stop_loss_trade_flag_}')
            if not stop_loss_trade_flag_:
                amount = p_trdr.main_currency_amount if trade_type == "SELL" else p_trdr.secondary_currency_amount
                p_trdr.trade(
                            # amount=10 if trade_type == "SELL" else 1,
                            amount=amount, ###??? why its not profitable
                            trade_type=trade_type, # buy main or sell main
                            sell_price=float(row['open_']),
                            buy_price=float(row['open_']),
                        )

                trade_data.loc[len(trade_data)] = p_trdr.get_df(timestamp=row['date_created']).squeeze() # TODO replase _amount here
                trade_data.loc[len(trade_data)-1, 'reason'] = 'trade_alg'
            else:
                stop_loss_trade_flag_ = False
                logging.info('poggers')
        return trade_data, stop_loss_trade_flag_


# if __name__ == '__main__':
    # TODO add some examples

