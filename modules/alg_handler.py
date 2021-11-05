'''
быстро вызвать из algma.py  функции и передать данные из низ в trade.py
'''
from collections import namedtuple
import json
import pandas as pd
from pandas.core.frame import DataFrame
from alg_ma import AlgMa
from datetime import datetime


class AlgHandler(object): 
    def __init__(self, *args, **kwargs):
       super(AlgHandler, self).__init__()
       self.LOG_FILE_PATH = kwargs.pop('log_path', './test_log.txt')
       self.pair = kwargs.pop('pair', 'RVNUSDT')
       self.data_file = kwargs.pop('data', r"C:\Users\akorz\Documents\binance_bot\binance_candle_plot\RVNUSD_data.txt")
       self.MA_lines = None
       self.crosses = None
       self.last_cross = None

    def _read_data(self, ):
        # if type == str значит это путь к файлу
        # else try to iterrate tru it [list, tuple,:: iterable]
        if isinstance(self.data_file, (list, tuple)):
            self.df = pd.DataFrame(self.data_file)
        if type(self.data_file) == type(''):
            with open(self.data_file, "r") as f:
                data_file = f.readlines()
                self.df = pd.DataFrame([json.loads(i) for i in data_file])
        return self.df
    
    def update_data(self, df:DataFrame):
        self.df = df # refactor later

    def calculate(self, ) -> tuple[list[DataFrame, DataFrame, DataFrame], list[namedtuple]]:
        '''update MAlines and crosses     '''
        self._read_data()
        self.MA_lines = AlgMa.alg_main(self.df['o'], )
        self.crosses = AlgMa.find_intersections(self.df['E'], mov_avg=self.MA_lines)
        return self.MA_lines, self.crosses

    def evaluate(self, ):
        try:
            cross = self.crosses[-1]
        except IndexError:
            cross = self.last_cross
            # print('no crosses found')
        #check if value of self.crosses has changed
        if cross != self.last_cross: 
            # call trade.py to provide trading operations
            if cross.type == 'fall': 
                # buy RVN
                with open(self.LOG_FILE_PATH, "a+") as f:
                    f.write('{'+f'"time":"{datetime.today()}","pure price":"{cross.val}","buy":"RVN"'+'}\n')
            if cross.type == 'raise': 
                # sell RVN
                with open(self.LOG_FILE_PATH, "a+") as f:
                    f.write('{'+f'"time":"{datetime.today()}","pure price":"{cross.val}","sell":"RVN"'+'}\n')
            self.last_cross = cross
            return True, cross.type
        self.last_cross = cross
        return False, None



if __name__ == '__main__':
    # init class w/ vars and path to file w/ data
    alg = AlgHandler(
        # path to txt file or list/tuple
        data=[{"e":"24hrTicker","E":1635803945097,"s":"RVNUSDT","p":"-0.00139000","P":"-1.147","w":"0.12036354","x":"0.12131000","c":"0.11983000","Q":"426.80000000","b":"0.11984000","B":"6219.50000000","a":"0.11990000","A":"1893.00000000","o":"0.12122000","h":"0.12516000","l":"0.11510000","v":"204660482.70000000","q":"24633659.69379500","O":1635717545097,"C":1635803945097,"F":29652470,"L":29749686,"n":97217},
{"e":"24hrTicker","E":1635803946098,"s":"RVNUSDT","p":"-0.00139000","P":"-1.147","w":"0.12036354","x":"0.12131000","c":"0.11983000","Q":"426.80000000","b":"0.11985000","B":"2600.00000000","a":"0.11989000","A":"1572.60000000","o":"0.12122000","h":"0.12516000","l":"0.11510000","v":"204660482.70000000","q":"24633659.69379500","O":1635717545486,"C":1635803945486,"F":29652470,"L":29749686,"n":97217},
{"e":"24hrTicker","E":1635803946967,"s":"RVNUSDT","p":"-0.00139000","P":"-1.147","w":"0.12036354","x":"0.12131000","c":"0.11983000","Q":"426.80000000","b":"0.11985000","B":"2600.00000000","a":"0.11989000","A":"1572.60000000","o":"0.12122000","h":"0.12516000","l":"0.11510000","v":"204660482.70000000","q":"24633659.69379500","O":1635717545486,"C":1635803945486,"F":29652470,"L":29749686,"n":97217},
{"e":"24hrTicker","E":1635803948075,"s":"RVNUSDT","p":"-0.00140000","P":"-1.155","w":"0.12036326","x":"0.12123000","c":"0.11983000","Q":"426.80000000","b":"0.11985000","B":"2600.00000000","a":"0.11990000","A":"2600.00000000","o":"0.12123000","h":"0.12516000","l":"0.11510000","v":"204592920.60000000","q":"24625470.82008200","O":1635717548075,"C":1635803948075,"F":29652479,"L":29749686,"n":97208},
{"e":"24hrTicker","E":1635803948808,"s":"RVNUSDT","p":"-0.00140000","P":"-1.155","w":"0.12036326","x":"0.12123000","c":"0.11983000","Q":"426.80000000","b":"0.11985000","B":"2600.00000000","a":"0.11990000","A":"2600.00000000","o":"0.12123000","h":"0.12516000","l":"0.11510000","v":"204592920.60000000","q":"24625470.82008200","O":1635717548075,"C":1635803948075,"F":29652479,"L":29749686,"n":97208},
{"e":"24hrTicker","E":1635803950004,"s":"RVNUSDT","p":"-0.00140000","P":"-1.155","w":"0.12036323","x":"0.12123000","c":"0.11983000","Q":"426.80000000","b":"0.11985000","B":"5880.00000000","a":"0.11990000","A":"2600.00000000","o":"0.12123000","h":"0.12516000","l":"0.11510000","v":"204585761.20000000","q":"24624602.88602000","O":1635717550003,"C":1635803950003,"F":29652481,"L":29749686,"n":97206},
{"e":"24hrTicker","E":1635803950514,"s":"RVNUSDT","p":"-0.00140000","P":"-1.155","w":"0.12036323","x":"0.12123000","c":"0.11983000","Q":"426.80000000","b":"0.11985000","B":"5880.00000000","a":"0.11990000","A":"2600.00000000","o":"0.12123000","h":"0.12516000","l":"0.11510000","v":"204585761.20000000","q":"24624602.88602000","O":1635717550003,"C":1635803950003,"F":29652481,"L":29749686,"n":97206},
{"e":"24hrTicker","E":1635803951591,"s":"RVNUSDT","p":"-0.00140000","P":"-1.155","w":"0.12036323","x":"0.12123000","c":"0.11983000","Q":"426.80000000","b":"0.11985000","B":"5880.00000000","a":"0.11990000","A":"2600.00000000","o":"0.12123000","h":"0.12516000","l":"0.11510000","v":"204585761.20000000","q":"24624602.88602000","O":1635717550003,"C":1635803950003,"F":29652481,"L":29749686,"n":97206},
{"e":"24hrTicker","E":1635803952411,"s":"RVNUSDT","p":"-0.00133000","P":"-1.098","w":"0.12036322","x":"0.12123000","c":"0.11985000","Q":"239.30000000","b":"0.11985000","B":"2360.70000000","a":"0.11990000","A":"2600.00000000","o":"0.12118000","h":"0.12516000","l":"0.11510000","v":"204584107.50000000","q":"24624402.07773500","O":1635717552411,"C":1635803952411,"F":29652482,"L":29749687,"n":97206},
{"e":"24hrTicker","E":1635803953970,"s":"RVNUSDT","p":"-0.00133000","P":"-1.098","w":"0.12036322","x":"0.12123000","c":"0.11985000","Q":"239.30000000","b":"0.11985000","B":"2360.70000000","a":"0.11990000","A":"2600.00000000","o":"0.12118000","h":"0.12516000","l":"0.11510000","v":"204584107.50000000","q":"24624402.07773500","O":1635717552411,"C":1635803952411,"F":29652482,"L":29749687,"n":97206},
{"e":"24hrTicker","E":1635803954717,"s":"RVNUSDT","p":"-0.00133000","P":"-1.098","w":"0.12036322","x":"0.12123000","c":"0.11985000","Q":"239.30000000","b":"0.11986000","B":"6789.90000000","a":"0.11991000","A":"910.60000000","o":"0.12118000","h":"0.12516000","l":"0.11510000","v":"204584107.50000000","q":"24624402.07773500","O":1635717554703,"C":1635803954703,"F":29652482,"L":29749687,"n":97206},
        ]
    )
    print(alg.calculate())

    # call trade.py if last val of crossing cahanged
    # trade 
    # after we should call logon_binance.py to provide sell/buy operations
    alg.evaluate()
    alg.evaluate()
    # alg._read_data()
