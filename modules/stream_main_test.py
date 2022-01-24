from collections import deque
from time import sleep

from open_binance_api import OpenBinanceApi
from alg_handler import AlgHandler
from wss_thread import WssThread

import pandas as pd
import logging

if __name__ == '__main__':
    logging.basicConfig(format="%(asctime)s: %(message)s", level=logging.INFO)

    USD_money = 10
    logging.info(f'{USD_money=}')
    fee = 0.1
    fee_c = 1 - fee*0.01
    # connect to wss on background
    w = WssThread(
        url='wss://stream.binance.com:9443/ws/rvnusdt@ticker',
        maxlen=10,
    )
    w.start()
    RVN_q = deque(maxlen=1000)
    get_data = lambda: OpenBinanceApi.get_data(
            pair = 'RVNUSDT',
            interval = '1m',
            limit = 1000,
            )
    [RVN_q.append(i) for i in get_data()]
    alg = AlgHandler(
        data=pd.DataFrame(
            list(RVN_q), 
            columns=[    
                'E',
                'o',
                'h',
                'l',
                'c',
                'v',
                'Close time',
                'Quote asset volume',
                'Number of trades',
                'Taker buy base asset volume',
                'Taker buy quote asset volume',
                'Ignore.',
            ]
        )
    )
    upd = lambda x: alg.update_data(pd.DataFrame(
            list(x), 
            columns=[    
                'E',
                'o',
                'h',
                'l',
                'c',
                'v',
                'Close time',
                'Quote asset volume',
                'Number of trades',
                'Taker buy base asset volume',
                'Taker buy quote asset volume',
                'Ignore.',
            ]
        ))
    try:
        while True:
            sleep(1)
            # get data from API
            list_data = get_data()
            last_candle = list_data[-1]
            second_candle = list_data[-2]

            # # if data is different add it to deque object
            if RVN_q[-1][0] != second_candle[0]:
                RVN_q.append(second_candle)
                upd(RVN_q)
                logging.info(RVN_q[-1])
                logging.info(alg.calculate())
                result_aval, operation_type =  alg.evaluate()
                logging.info(f'{result_aval=}, {operation_type=}')
                if result_aval:
                    if operation_type == 'raise':
                        actual_prise = w.get_data()['a']
                        logging.info(f'{actual_prise=}')
                        RVN_money = USD_money * fee_c /float(actual_prise) # ['a'] buy rvn
                        logging.info(f'{RVN_money=}, {operation_type=}, {actual_prise=}')
                    elif operation_type == 'fall':
                        actual_prise = w.get_data()['b']
                        logging.info(f'{actual_prise=}')
                        try:
                            USD_money = RVN_money * fee_c * float(actual_prise) # ['b'] sell rvn
                            logging.info(f'{USD_money=}, {operation_type=}, {actual_prise=}')
                        except NameError: 
                            logging.error('operation was ignored due to insufficient amount of valut')
 
                        
            # call evaluate
        # if we got crosses do a trade w/ wss stream based values
    finally:
        w.close()
