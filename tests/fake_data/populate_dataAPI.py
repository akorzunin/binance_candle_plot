

import requests
import pandas as pd
import pickle
import json
import logging
DEBUG = __debug__ 
LOG_FILE_NAME = 'populate_data_API.log'
format = '%(asctime)s [%(levelname)s]: %(message)s'
logger = logging.basicConfig(
    filename=LOG_FILE_NAME if not DEBUG else None, 
    format=format,
    encoding='utf-8', 
    level=logging.DEBUG, 
)
if not DEBUG:
    logging.getLogger(logger).addHandler(logging.StreamHandler())

#load .env variables
import os
from dotenv import load_dotenv
load_dotenv()
PWD = os.getenv('PWD')

endpoint = 'http://192.168.1.125:8000'


# r = requests.post(f'{endpoint}/ma_lines', json=[7, 25, 99])
# re = r.json()
# if r.status_code == 200: logging.info('MA_lines OK')


trade_data = pd.read_csv(f'{PWD}/temp/trade_data_raw.csv', index_col=0)
df = pd.read_csv(f'{PWD}/temp/df_raw.csv', index_col=0)

# df = trade_data
r = requests.post(f'{endpoint}/trade_data', json.dumps({'new_item': trade_data.to_json()}))
if r.status_code == 200: logging.info('trade_data OK')


r = requests.post(f'{endpoint}/stock_data', json.dumps({'new_item': df.to_json()}))

if r.status_code == 200: logging.info('stock_data OK')








