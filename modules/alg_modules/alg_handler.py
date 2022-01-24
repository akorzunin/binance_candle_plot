'''
быстро вызвать из algma.py  функции и передать данные из низ в trade.py
'''

from collections import namedtuple
import json
from typing import Tuple
import pandas as pd
from pandas.core.frame import DataFrame
from alg_ma import AlgMa
from datetime import datetime
import logging


class AlgHandler(object): 
    def __init__(self, *args, **kwargs):
        super(AlgHandler, self).__init__()
    #    self.LOG_FILE_PATH = kwargs.pop('log_path', './test_log.txt')
    #    self.pair = kwargs.pop('pair', 'RVNUSDT')
        self.df = kwargs.get('df', pd.DataFrame())
        self.ALLOW_SAME_RESPONSE = kwargs.get('ALLOW_SAME_OP', False)
        self.MA_lines = None
        self.crosses = None
        self.last_cross = None
    
    def update_data(self, df: DataFrame):
        '''Update dataframe inside instance'''
        self.df = df

    def calculate(self, val_col: str, time_col: str) -> tuple[list[DataFrame, DataFrame, DataFrame], list[namedtuple]]:
        '''update MAlines and crosses     '''
        # self._read_data()
        # select column w/ data to get moving average values from
        self.MA_lines = AlgMa.alg_main(self.df[val_col], )
        self.crosses = AlgMa.find_intersections(
            # select cloumnt w/ time data
            date_df=self.df[time_col], 
            # select lines to calculate intersection with
            mov_avg1=self.MA_lines[1].to_list(), 
            mov_avg2=self.MA_lines[2].to_list(),
            ) 
        return self.MA_lines, self.crosses

    def evaluate(self, ) -> tuple[bool, str]:
        '''call it only once to get alg decision base on current data calculated w/ calculate method\n
        returns bool, 'fall' or 'raise'
        '''
        # flag to allow or not same operation
        # like if we have fall we cant have fall again
        try:
            self.last_op = self.last_cross.type # raise or fall
        except AttributeError as e: 
            self.last_op = None 
            
        try:
            cross = self.crosses[-1]
        except IndexError:
            cross = self.last_cross
            # print('no crosses found')
        #check if value of self.crosses has changed
        if cross != self.last_cross: 
            # refactor : cross getting updated in calculate

            if not self.ALLOW_SAME_RESPONSE and self.last_op == cross.type:
                logging.debug('same result')
                return False, 'same result'
            if cross.type == 'fall': 
                # buy RVN
                logging.debug(f'"pure price":"{cross.val}","buy":"RVN"'+f'{cross.type=}'+'')
            if cross.type == 'raise': 
                # sell RVN
                logging.debug(f'"pure price":"{cross.val}","sell":"RVN"'+f'{cross.type=}'+'')
            self.last_cross = cross
            return True, cross.type
        self.last_cross = cross
        return False, None



if __name__ == '__main__':
    from datetime import datetime
    from random import randint
    import math
    df = pd.DataFrame()
    df['Test'] = [math.sin(i) for i in range(1000)]
    # df['Test'] = [i if i > 500 else 500 - i for i in range(1000) ]
    df['Time'] = [datetime.fromtimestamp(i*10**6) for i in range(1000)]
    # init class w/ vars and path to file w/ data
    alg = AlgHandler(
        df=df,
    )
    logging.basicConfig(level=logging.INFO)
    alg.calculate(
        val_col='Test',
        time_col='Time',
    )
    logging.info(alg.evaluate())
    for i in alg.crosses:
        logging.info(f'{i=}')

