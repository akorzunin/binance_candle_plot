
import pandas as pd
import requests

class DataApiWrapper(object): 
    '''docstring for DataApiWrapper'''
    def __init__(self, **kwargs):
        super().__init__()
        self.endpoint = kwargs.pop('endpoint')

    def get_ma_lines(self, ) -> tuple or None:
        '''return tuple if request successful or None if failed'''
        r = requests.get(f'{self.endpoint}/ma_lines',)
        re = r.json()
        if r.status_code < 400: return tuple(re['ma_lines'])
        else: return None
    
    def get_stock_data(self,) -> pd.DataFrame or None:
        '''return DataFrame if request successful or None if failed'''
        r = requests.get(f'{self.endpoint}/stock_data', )
        if r.status_code < 400: 
            return pd.read_json(r.json()['stock_data'])
        else: return None 
        
    def get_trade_data(self,) -> pd.DataFrame or None:
        '''return DataFrame if request successful or None if failed'''
        r = requests.get(f'{self.endpoint}/trade_data', )
        if r.status_code < 400: 
            return pd.read_json(r.json()['trade_data'])
        else: return None 

if __name__ == '__main__':
    # use wrapper to get data from dataAPI
    # [WARNING] use interactive window to see dataframes
    endpoint = 'http://192.168.1.125:8000'
    
    w = DataApiWrapper(
        endpoint=endpoint,
    )
    print(f'MA_lines: {w.get_ma_lines()}')
    print('Stock data:')
    display(w.get_stock_data())
    print('Trade data:')
    display(w.get_trade_data())

