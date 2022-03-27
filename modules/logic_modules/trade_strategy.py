
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
    def static_trade_strategy(**kwargs):
        STOP_LOSS_ENABLED = kwargs.get('STOP_LOSS_ENABLED', False)
        STOP_LOSS_THRESHOLD = kwargs.get('STOP_LOSS_THRESHOLD', 0)
        stop_loss_trade_flag = kwargs.get('stop_loss_trade_flag', 0)
        stop_loss = kwargs.get('stop_loss', )
        trade_data = kwargs.get('trade_data',)
        # alg = kwargs.get('alg',)
        window = kwargs.get('window',)
        p_trdr = kwargs.get('p_trdr',)
        MA_list = kwargs.get('MA_list', (2, 25, 100, 200) )
        df = kwargs.get('df', None) 

        # use caustom column names
        open_col  = kwargs.pop('open_col', 'Open')
        high_col = kwargs.pop('high_col', 'High')
        low_col = kwargs.pop('low_col', 'Low')
        close_col = kwargs.pop('close_col', 'Close')
        date_col = kwargs.pop('date_col', 'Date')

        # global stop_loss_trade_flag
        stop_loss_trade_flag = False
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
            columns = p_trdr.get_df(timestamp=df.iloc[-1][date_col]).columns.values # 'data_created'
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
            alg.calculate(val_col=open_col, time_col=date_col,)
            do_trade, cross_type = alg.evaluate()
            # if stop_loss_trade_flag: logging.info(f'holy {stop_loss_trade_flag}')
            if STOP_LOSS_ENABLED:
                stop_loss_trade_flag, trade_data = stop_loss.stop_loss_alg(
                    stop_loss_trade_flag=stop_loss_trade_flag,
                    trade_data=trade_data,
                    p_trdr=p_trdr,
                    row=row,
                    open_col=open_col,
                    date_col=date_col,
                )

            # if stop_loss_trade_flag: logging.info(f'pog {stop_loss_trade_flag}')
            ## do not allow same operation twise in a row
            if do_trade:
                # logging.info(f'pepe {stop_loss_trade_flag}')
                trade_data, stop_loss_trade_flag = TradeStrategy.trade_alg(
                    stop_loss_trade_flag, 
                    trade_data, 
                    p_trdr, 
                    row, 
                    cross_type,
                    open_col=open_col,
                    date_col=date_col,
                )
                # print(stop_loss_trade_flag)
        return stop_loss.stop_loss_count, trade_data, p_trdr

    @staticmethod
    def trade_strategy(**kwargs):
        STOP_LOSS_ENABLED = kwargs.get('STOP_LOSS_ENABLED', False)
        # STOP_LOSS_THRESHOLD = kwargs.get('STOP_LOSS_THRESHOLD', 0)
        stop_loss_trade_flag = kwargs.get('stop_loss_trade_flag', 0)
        stop_loss = kwargs.get('stop_loss', )
        trade_data = kwargs.get('trade_data',)
        alg = kwargs.get('alg',)
        window = kwargs.get('window',)
        p_trdr = kwargs.get('p_trdr',)
        wss = kwargs.get('wss', None)
        # MA_list = kwargs.get('MA_list', (2, 25, 100, 200) )
        # df = kwargs.get('df', None) 
        df_ = pd.DataFrame(window)
        alg.update_data(df_)
        alg.calculate(val_col='Open', time_col='Date',)
        do_trade, cross_type = alg.evaluate()
        # if stop_loss_trade_flag: logging.info(f'holy {stop_loss_trade_flag}')
        if STOP_LOSS_ENABLED:
            stop_loss_trade_flag, trade_data = stop_loss.stop_loss_alg(
                stop_loss_trade_flag=stop_loss_trade_flag,
                trade_data=trade_data,
                p_trdr=p_trdr,
                row=df_[-1:],
                wss=wss,
            )

        # if stop_loss_trade_flag: logging.info(f'pog {stop_loss_trade_flag}')
        ## do not allow same operation twise in a row
        if do_trade:
            # logging.info(f'pepe {stop_loss_trade_flag}')
            if not stop_loss_trade_flag:

                trade_data, stop_loss_trade_flag = TradeStrategy.trade_alg(
                    stop_loss_trade_flag, 
                    trade_data, 
                    p_trdr, 
                    df_[-1:], 
                    cross_type,
                    wss=wss,
                )
            else:
                stop_loss_trade_flag = False
                logging.warning('STOP LOSS cancel alg trade')
            # print(stop_loss_trade_flag)
        return stop_loss.stop_loss_count, trade_data, p_trdr, stop_loss_trade_flag

    @staticmethod
    def trade_alg(stop_loss_trade_flag_, trade_data, p_trdr, row, cross_type, **kwargs):
        open_col  = kwargs.pop('open_col', 'Open')
        date_col = kwargs.pop('date_col', 'Date')

        wss = kwargs.pop('wss', None)

        trade_type = "SELL" if cross_type=='raise' else "BUY"
        # do not SELL on first trade
        if  (len(trade_data) > 0) or (trade_type == "BUY"):
            # logging.info(f'{stop_loss_trade_flag_}')
            if not stop_loss_trade_flag_:
                amount = p_trdr.main_currency_amount if trade_type == "SELL" else p_trdr.secondary_currency_amount
                if wss is not None:
                    p_trdr.trade(
                        amount=amount, 
                        trade_type=trade_type, 
                        sell_price=wss.get_data()['c'],
                        buy_price=wss.get_data()['c'],
                    )
                    logging.warning(f'[TRADE] {trade_type=}, price: {wss.get_data()}')
                else:
                    p_trdr.trade(
                        amount=amount, 
                        trade_type=trade_type, 
                        sell_price=float(row[open_col]),
                        buy_price=float(row[open_col]),
                    )
                # p_trdr.trade(
                #     # amount=10 if trade_type == "SELL" else 1,
                #     amount=amount, ###??? why its not profitable
                #     trade_type=trade_type, # buy main or sell main
                #     sell_price=float(row[open_col]),
                #     buy_price=float(row[open_col]),
                # )
                try:
                    trade_data.loc[len(trade_data)] = p_trdr.get_df(timestamp=row[date_col].item().to_pydatetime()).squeeze() # TODO replase _amount here
                except AttributeError:
                    trade_data.loc[len(trade_data)] = p_trdr.get_df(timestamp=row['date_created']).squeeze() # TODO replase _amount here
                trade_data.loc[len(trade_data)-1, 'reason'] = 'trade_alg'
                # if len(trade_data): logging.warning(f'[TRADE] {len(trade_data)}')
            else:
                # stop_loss_trade_flag_ = False
                pass
                # logging.info('poggers')
        return trade_data, stop_loss_trade_flag_


# if __name__ == '__main__':
    # TODO add some examples

