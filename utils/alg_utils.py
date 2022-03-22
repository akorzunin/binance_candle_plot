import logging
from pandas.core.frame import DataFrame

def calculate_profit(trade_data: DataFrame) -> DataFrame:
    for i, row in trade_data.iterrows():
    # try:
        if row['type'] == 'sell':
            try:
                trade_data.loc[i, 'profit_abs'] = float(row['USD']) - float(trade_data['USD'].loc[i-2])
                # (curr_buy_pr - prev_buy_pr)*100/prev_buy_pr
                trade_data.loc[i, 'profit_rel'] = round((float(row['USD']) - float(trade_data['USD'].loc[i-2])) *100/float(trade_data['USD'].loc[i-2]),2)
            except KeyError: logging.debug(f'[CALC PROFIT] cannot find index: {i}')
        if row['type'] == 'buy':
            try:
                trade_data.loc[i, 'profit_abs'] = float(row['RVN']) - float(trade_data['RVN'].loc[i-2])
                # (curr_buy_pr - prev_buy_pr)*100/prev_buy_pr
                trade_data.loc[i, 'profit_rel'] = round((float(row['RVN']) - float(trade_data['RVN'].loc[i-2]))*100/float(trade_data['RVN'].loc[i-2]),2)
            except KeyError: logging.debug(f'[CALC PROFIT]cannot find index: {i}')
    
    return trade_data