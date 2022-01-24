# %%
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()
PWD = os.getenv('PWD')
db_name = PWD+'\\database'+'\\test.db'
df = pd.read_sql(
    'SELECT * FROM minute_scale WHERE date_created > "2021-12-30 00:00:00.000000"',
    'sqlite:///' + db_name, 
    index_col='id',
)
# df = df.head(3)
df

# %%
import sys
sys.path.insert(1, PWD+'\\modules')
from alg_modules.alg_handler import AlgHandler

# %%

from collections import deque
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


# %%
alg = AlgHandler(data_file=pd.DataFrame())

# %%
df = pd.read_sql(
    'SELECT * FROM minute_scale WHERE date_created > "2021-12-30 00:00:00.000000"',
    'sqlite:///' + db_name, 
    index_col='id',
)
logging.basicConfig(level=logging.DEBUG)
window = deque(maxlen=1000)
# init alg
alg = AlgHandler(data=pd.DataFrame([]))
for i, row in df.iterrows():
    window.append(dict(row))
    # logging.debug(window[-1])
    df = pd.DataFrame(window)
    try:
        logging.debug()
        alg.update_data(df)
        alg.calculate(val_col='open_', time_col='open_time',)
        alg.evaluate()
    except KeyError as e:
        logging.error(i)
        logging.error(e)

# %%
%%timeit
df = pd.DataFrame(window)
df


