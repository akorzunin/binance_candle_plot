import logging
import sys
import threading
import time
from collections import deque
import pandas as pd
from datetime import datetime
# ---
from win10toast import ToastNotifier

import pandas as pd
import numpy as np
import pickle
import os
import asyncio
import datetime
from datetime import datetime
from datetime import timedelta, timezone
from typing import Optional
from dotenv import load_dotenv
from operator import itemgetter

load_dotenv()
PWD = os.getenv("PWD")
db_name = PWD + "\\database" + "\\RVNUSDT.db"
import sys

sys.path.insert(1, PWD + "\\modules")
from alg_modules.alg_handler import AlgHandler
from plot_modules.candle_plot import CandlePlot
from collections import deque
from paper_trade import PaperTrader
import time
import logging

DEBUG = __debug__
LOG_FILE_NAME = "log_file_name.log"
format = "%(asctime)s [%(levelname)s]: %(message)s"
logger = logging.basicConfig(
    filename=LOG_FILE_NAME if not DEBUG else None,
    format=format,
    encoding="utf-8",
    level=logging.INFO,
)
if not DEBUG:
    logging.getLogger(logger).addHandler(logging.StreamHandler())

from stop_loss import StopLoss
from trade_strategy import TradeStrategy
from wss_thread import WssThread
from api_modules.open_binance_api import OpenBinanceApi
import pytz
tzdata = pytz.timezone('Europe/Moscow') 

# ---
class Trader(object): 
    '''docstring for Trader'''
    def __init__(self, ):
        super().__init__()

        self.is_stopped = None
        self._thread = threading.Thread(target=self.between_callback, args=())
        # self._thread = threading.Thread(target=asyncio.run, args=())
        self._lock = threading.Lock()

    def between_callback(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        self.loop.run_until_complete(self.thread_function(self))
        self.loop.close()

    async def thread_function(self, *args, **kwargs):
        # ====

        def compute_timedelta(dt: datetime):
            if dt.tzinfo is None:
                dt = dt.astimezone()
            now = datetime.now(timezone.utc)
            return max((dt - now).total_seconds(), 0)

        async def sleep_until(when: datetime, result = None):
            """|coro|
            Sleep until a specified time.
            If the time supplied is in the past this function will yield instantly.
            .. versionadded:: 1.3
            Parameters
            -----------
            when: :class:`datetime.datetime`
                The timestamp in which to sleep until. If the datetime is naive then
                it is assumed to be local time.
            result: Any
                If provided is returned to the caller when the coroutine completes.
            """
            delta = compute_timedelta(when)
            return await asyncio.sleep(delta, result)

        # ====
        server_time = datetime.fromtimestamp(OpenBinanceApi.server_time()/1000)
        local_time = datetime.now()
        delay = server_time - local_time
        # ====
        # notifications
        toast = ToastNotifier()
        static_notification_settings = dict(
            title="Algo traid BOT",
            duration = 20,
            icon_path = "python.ico",
            threaded = 1,
        )

        notify = lambda msg: toast.show_toast(
            msg=msg,
            **static_notification_settings,
            )

        msg="Watch out for notifications from here"
        async def notification(msg):
            if not notify(msg):
                await asyncio.sleep(20)
                notify(msg)

        await notification(msg)
        # ====
        DATA_AWAIT_TIME = 1 # seconds
        SERVER_DELAY = 10 # seconds
        INTERVAL_SECONDS = 60 # seconds
        # request that data from api
        w = WssThread(
            url='wss://stream.binance.com:9443/ws/rvnusdt@ticker',
            maxlen=10,
            )
        w.start()

        STOP_LOSS_ENABLED=True
        STOP_LOSS_THRESHOLD=-1.3

        DEQUE_MAX_LENGTH = 200
        INTERVAL = '1m'


        df = OpenBinanceApi.get_df(
            pair = 'RVNUSDT',
            interval = INTERVAL,
            limit = 1000,
            )
        # drop last row TODO make assert to not dublicate last row from cycle
        df = df[:-1]
        stop_loss_trade_flag = False
        MA_list = (2, 7, 25, 100)

        window = deque(maxlen=200)
        for i, row in df.iterrows():
            window.append(dict(row.squeeze()))
        #initial currency resources
        p_trdr = PaperTrader(
            main_currency_label='RVN',
            secondary_currency_label='USD',
            main_currency_amount=100,
            secondary_currency_amount=0,
            fee=0.1,
        )
        trade_data = pd.DataFrame(
            columns = p_trdr.get_df(timestamp=df.iloc[-1]['Date']).columns.values
        )
        stop_loss = StopLoss(
            STOP_LOSS_THRESHOLD=STOP_LOSS_THRESHOLD,
        )
        # init alg
        alg = AlgHandler(
            df=pd.DataFrame([]),
            MA_list=MA_list,
            )
        while not self._stopped:
                logging.info('===get new data===')
                new_df = OpenBinanceApi.get_df(
                        pair = 'RVNUSDT',
                        interval = INTERVAL,
                        limit = 2,
                    )
                dt = datetime.fromtimestamp(int(new_df.Real_Date[-1:])/1000)
                server_time = datetime.fromtimestamp(OpenBinanceApi.server_time()/1000)
                logging.debug(f'server time: {server_time}   {server_time.minute=}, {dt.minute=}')
                # extract function?

                if server_time.minute == dt.minute:
                    logging.debug('+++===success===+++')
                    window.append(dict(new_df[-2:-1].squeeze()))
                    df_ = pd.DataFrame(window)
                    # === process data here ===
                    # display(df_)
                    for _, row in df_.iterrows():
                        # window.append(dict(row))
                        # df__ = pd.DataFrame(window)
                        alg.update_data(df_)
                        alg.calculate(val_col='Open', time_col='Date',)
                        do_trade, cross_type = alg.evaluate()
                        if STOP_LOSS_ENABLED:
                            stop_loss_trade_flag, trade_data = stop_loss.stop_loss_alg(
                                                                    trade_data=trade_data,
                                                                    p_trdr=p_trdr,
                                                                    row=row,
                                                                )

                    if do_trade:
                        trade_data, stop_loss_trade_flag = TradeStrategy.trade_alg(stop_loss_trade_flag, trade_data, p_trdr, row, cross_type)
                        await notification(f'Trade done: {trade_data}\n {trade_data[-1:]}')
                    logging.info(f'do trade: {do_trade}')
                    self.p_trdr = p_trdr
                    self.alg = alg
                    # self.df__ = df__
                    self.df_ = df_
                    self.window = window
                    # display(trade_data)
                    # display(alg.crosses)
                    # === end of data processing ===
                    time_to_sleep = dt - delay + timedelta(seconds=SERVER_DELAY) + timedelta(seconds=INTERVAL_SECONDS)
                    server_delay = dt - server_time
                    logging.debug(f'server valid time: {server_time}')
                    logging.debug(f'server delay: {server_delay.total_seconds()}')
                    logging.debug(f'sleep till: {time_to_sleep}')
                    await sleep_until(time_to_sleep)
                else:
                    logging.debug('---not valid---')
                    logging.debug('sleep 1 sec')
                    await asyncio.sleep(DATA_AWAIT_TIME)
        

    def get_data(self, ) -> dict:
        with self._lock:
            # e = (self.queue or [None])[-1]
            try:
                # return(ast.literal_eval(e)) #???
                return self.p_trdr, self.alg, self.df_, self.window
            except ValueError as err: 
                logging.debug(err)
    
    def start(self):
        '''Start the thread'''
        logging.info(f"[{self.__class__.__name__}] Opening thread")
        self.is_stopped = False
        self._thread.start()


    def close(self) -> None:
        ''' Close the thread'''
        with self._lock:
            logging.info(f"[{self.__class__.__name__}] Closing thread")
            self.is_stopped = True
            # self.loop.keep_running = False
            loop = asyncio.get_event_loop()
            loop.stop()
            loop.close()

    @property
    def _stopped(self):
        return self.is_stopped
    
    @property
    def is_alive(self):
        return self._thread.is_alive()

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    w = Trader(
        # url='wss://stream.binance.com:9443/ws/rvnusdt@ticker',
        # maxlen=10,
        )
    w.start()

    try:
        while True:
            print(w.get_data())
            time.sleep(5)
    finally:
        # close thread
        w.close()