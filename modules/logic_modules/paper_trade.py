
import datetime
import logging
import pandas as pd
import numpy as np
import numba

class PaperTrader(object): 
    '''simulate currensy exchange operations w/ custom price, fee'''
    def __init__(self, **kwargs):
        super(PaperTrader, self).__init__()
        self.sell_price = kwargs.get('sell_price', None)  
        self.buy_price = kwargs.get('buy_price', None)

        self.fee = float(kwargs.get('fee', 0))
        self.fee_c = 1 - 0.01*self.fee

        self._main_currency_label = kwargs.get('main_currency_label', 'main_currency')
        self._secondary_currency_label = kwargs.get('secondary_currency_label', 'secondary_currency')

        self._main_currency_amount = kwargs.get('main_currency_amount', 0)
        self._secondary_currency_amount = kwargs.get('secondary_currency_amount', 0)

        self._amount = kwargs.get('amount', None)
        self._last_trade_type = kwargs.get('last_trade_type', None)

        self.LOG_DATA = kwargs.get('LOG_DATA', False)

    @property
    def main_currency_label(self):
        return self._main_currency_label
    @property
    def secondary_currency_label(self):
        return self._secondary_currency_label
    @property
    def main_currency_amount(self):
        return self._main_currency_amount
    @property
    def secondary_currency_amount(self):
        return self._secondary_currency_amount
    @property
    def amount(self):
        return self._amount
    @property
    def last_trade_type(self):
        return self._last_trade_type   

    def trade(self, *args, **kwargs):
        '''amount: how many of currensy been spent\n
        trade_type: sell or buy\n
            [sell] means we gonna spent {amount} of {main_currency} to buy {secondary_currency} w/ {sell_price}\n
            [buy] means we'll spend {amount} of {secondary_currency}' to buy {main_currency} w/ {buy_price}\n
        '''
        amount = kwargs.pop('amount', 0)
        trade_type = kwargs.pop('trade_type', None).lower()
        sell_price = kwargs.pop('sell_price', None)
        buy_price = kwargs.pop('buy_price', None)
        
        def log_it():
            if self.LOG_DATA:
                # logs
                logging.info(f'{self._main_currency_label}: {round(self._main_currency_amount, 2)}')
                logging.info(f'{self._secondary_currency_label}: {round(self._secondary_currency_amount, 2)}')
                logging.info(f'{trade_type=}')
                logging.info(f'{sell_price=}')

        if trade_type.lower() == 'sell':
            # straigt currensy conversion formula
            self._secondary_currency_amount += amount * self.fee_c * float(sell_price)
            self._main_currency_amount -= amount
            # save price
            self.sell_price = sell_price
            log_it()

        elif trade_type.lower() == 'buy': 
            # reverse currensy conversion formula
            self._main_currency_amount += amount * self.fee_c / float(buy_price)
            self._secondary_currency_amount -= amount
            # save price
            self.buy_price = buy_price
            log_it()

        # trade type can be only 'sell' or 'buy'
        else: raise KeyError
        # save last trade amount
        self._amount = amount
        # save last trade type
        self._last_trade_type = trade_type

        # return self.get_df()
            

    def get_info(self):
        logging.info(f'{self._main_currency_label}: {round(self._main_currency_amount, 2)}')
        logging.info(f'{self._secondary_currency_label}: {round(self._secondary_currency_amount, 2)}')
        logging.info(f'{self.fee=}')

    def convert_to_main(self, price):
        '''Convert all available currensy to main currensy'''
        self.trade(
            amount=self._secondary_currency_amount,
            trade_type='BUY',
            buy_price=price,
        )
        # self.get_info()

    def convert_to_secondary(self, price):
        '''Convert all available currensy to secondary currensy'''
        self.trade(
            amount=self._main_currency_amount,
            trade_type='SELL',
            sell_price=price,
        )
        self.get_info()
    
    def _get_point(self, **kwargs) -> dict:  
        '''Store timestamp and object variables into a dict'''
        pt = self.__dict__
        timestamp = kwargs.get('timestamp', None)
        if timestamp is None:
            pt['timestamp'] = datetime.datetime.today()
        else:
            pt['timestamp'] = timestamp
        return pt

    def get_df(self, **kwargs) -> pd.DataFrame:
        '''return object as df w/ timestamp'''
        df = pd.DataFrame(self._get_point(**kwargs), index=['0'])
        main_label = df['_main_currency_label'][0]
        secondary_label = df['_secondary_currency_label'][0]
        # remove
        df = df.drop(
            columns=[
                'LOG_DATA', 
                '_main_currency_label', 
                '_secondary_currency_label',
                'fee_c'
            ],
        )
        # rename
        df = df.rename(columns={
            '_main_currency_amount': main_label,
            '_secondary_currency_amount': secondary_label,
            '_last_trade_type': 'type',
        })
        # rearrange
        cols = df.columns.tolist()
        cols = [cols[cols.index('type')]] + cols[:cols.index('type')] + cols[cols.index('type')+1:]
        df = df[cols]
        return df 

    @staticmethod
    def calculate_profit(df: pd.DataFrame) -> None:
        '''Calculate prifit of each step and overall'''


        pass


if __name__ == '__main__':
    import logging
    DEBUG = __debug__ 
    LOG_FILE_NAME = 'log_file_name.log'
    format = '%(asctime)s [%(levelname)s]: %(message)s'
    logger = logging.basicConfig(
        filename=LOG_FILE_NAME if not DEBUG else None, 
        format=format,
        encoding='utf-8', 
        level=logging.DEBUG, 
    )
    if not DEBUG:
        logging.getLogger(logger).addHandler(logging.StreamHandler())


    p_trdr = PaperTrader(
        main_currency_label='RVN',
        secondary_currency_label='USD',
        main_currency_amount=10,
        # secondary_currency_amount=0
        fee=0.1,
        # logging_level=logging.DEBUG,
    )
    trade_type = "SELL" if 1 else "BUY"
    p_trdr.trade(
        amount=10,
        trade_type=trade_type, # buy main or sell main
        sell_price=9.9,
        buy_price=10.1,
    )
    p_trdr.get_info()
    # input()