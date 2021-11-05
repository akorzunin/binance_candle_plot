import json
import sys

import pandas as pd
sys.path.insert(1, r'C:\Users\akorz\Documents\binance_bot\binance_candle_plot\modules')
from alg_handler import AlgHandler

def main(FILENAME, LOG_PATH, OPS_PATH, PRINT=True, LOG=True, OPS_LOG=True):
    # read data file
    with open(FILENAME, 'r') as f:
        file = f.readlines()
        file = [json.loads(i) for i in file]
    buffer = []
    alg = AlgHandler(
        # path to txt file
        log_path=LOG_PATH,    
        data=buffer
    )
    # RVN = 100
    USD_money = 10
    start_money = USD_money
    fee = 0.1
    fee_c = 1 - fee*0.01
    # fee_c =1
    for line in file:
        buffer.append(line)
        alg.update_data(pd.DataFrame(buffer))
        alg.calculate()
        result, operation = alg.evaluate()
        if result:
            # print(operation)
            if operation == 'raise':
                # sell RVN
                RVN_money = USD_money * fee_c /alg.last_cross.val
                if PRINT: print(f'{RVN_money=}')
                if OPS_LOG: 
                    with open(OPS_PATH, 'a+') as f: f.write(f'{RVN_money=}\n')
            elif operation == 'fall': 
                # buy RVN
                try:
                    USD_money = RVN_money * fee_c * alg.last_cross.val
                except NameError: 
                    print('operation was ignored due to insufficient amount of valut')
                if PRINT: print(f'{USD_money=}')
                if OPS_LOG: 
                    with open(OPS_PATH, 'a+') as f: f.write(f'{USD_money=}\n')

        # print(alg.crosses)
    if PRINT: print(f'total: {USD_money}; {fee_c=}; start(USD): {start_money}')
    if OPS_LOG: 
        with open(OPS_PATH, 'a+') as f: f.write(f'total: {USD_money}; {fee_c=}; start(USD): {start_money}\n')


if __name__ == '__main__':
    FILENAME = 'RVNUSD_data_2.txt'
    main(
        FILENAME=fr"C:\Users\akorz\Documents\binance_bot\binance_candle_plot\{FILENAME}",
        LOG_PATH=f'./modules/tests/file_log_{FILENAME}.txt',
        OPS_PATH=f'./modules/tests/operations_log_{FILENAME}.txt',
        # PRINT=False,
        # LOG=True,
        # OPS_LOG=True,
    )
    
