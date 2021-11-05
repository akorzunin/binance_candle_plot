
from collections import namedtuple
import pandas as pd
from pandas.core.frame import DataFrame


class AlgMa():
    '''Calculate 3 moving average arrays from given dataframe'''
    @staticmethod
    def alg_main(df: DataFrame, MA_1=7, MA_2=25, MA_3=100, **kwargs) -> list[DataFrame, DataFrame, DataFrame]:
        mov_avg = [[], [], []]
        mov_avg[0] = df.rolling(window = MA_1).mean()
        mov_avg[1] = df.rolling(window = MA_2).mean()
        mov_avg[2] = df.rolling(window = MA_3).mean()

        return mov_avg 
    # @staticmethod
    # def alg_to_df(data: tuple, MA_1=7, MA_2=25, MA_3=100, **kwargs):

    # calc collisions
    # найти координаты пересечения линий
    @staticmethod
    def find_intersections(df: DataFrame, mov_avg: list[DataFrame, DataFrame, DataFrame]) -> list[namedtuple]:
        # unpack df structure
        date_df = df
        arr1 = mov_avg[1]
        arr2 = mov_avg[2]
        intersections = []
        MA_point = namedtuple('MA_point', 'timestamp val type')
        for num, i in enumerate(date_df):
            # if num == 999: print(num)
            if num == 0: next(enumerate(date_df))
            else:    
                A1 = arr1[num-1]
                A2 = arr1[num] 
                B1 = arr2[num-1]
                B2 = arr2[num] 
                if (A1 > B1) and (B2 > A2):
                    intersections.append(MA_point(i, arr1[num], 'fall'))
                if (A1 < B1) and (B2 < A2):
                    intersections.append(MA_point(i, arr1[num], 'raise'))

        return intersections


if __name__ == '__main__':
    # find MA lines
    from random import randint
    df = pd.DataFrame()
    df['Test'] = [randint(0, 100) for i in range(1000)]
    print(AlgMa.alg_main(df['Test'], MA_3=50))

    # find intersections
    df['Time'] = range(1000)
    p = AlgMa.find_intersections(df['Time'], AlgMa.alg_main(df['Test'], MA_3=50))
    print(p[0])
