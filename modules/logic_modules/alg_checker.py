'''test for trading operations
'''
import logging
import pandas as pd 
from pandas.core.frame import DataFrame
import sys
sys.path.insert(1, './modules')

### REFACTOR ###
# class AlgChecker(object): 
#     '''docstring for AlgChecker'''
#     def __init__(self, **kwargs):
#         super(AlgChecker, self).__init__()
#         self.init_money = kwargs.pop('init_money',)
#         self.fee_c = 1 - 0.01*kwargs.pop('fee',)

#     def check(self, df: DataFrame):

#         # for i in df
#             # add element to deque object

#             # do some calculate/evaluate staff w/ alg AlgHandler

#                 # log that to trades
#         logging.info('AlgChecker')

# if __name__ == '__main__':
#     import os
#     from dotenv import load_dotenv
#     load_dotenv()
#     PWD = os.getenv('PWD')
#     db_name = PWD+'\\database'+'\\test.db'
#     df = pd.read_sql(
#         'SELECT * FROM minute_scale WHERE date_created > "2021-10-01 00:00:00.000000"',
#         'sqlite:///' + db_name, 
#         index_col='id',
#     )
#     # print(df)

#     logging.basicConfig(level=logging.INFO)

#     a = AlgChecker(
#         init_money=10,
#         fee=0,
#     )
#     a.check(df) # return list of trades