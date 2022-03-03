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

load_dotenv()
PWD = os.getenv("PWD")
db_name = PWD + "\\database" + "\\RVNUSDT.db"
import sys

sys.path.insert(1, PWD + "\\modules")
from alg_modules.alg_handler import AlgHandler
from plot_modules.candle_plot import CandlePlot
from collections import deque
from logic_modules.paper_trade import PaperTrader
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

from logic_modules.stop_loss import StopLoss
# from logic_modules.trade_strategy import TradeStrategy
from wss_thread import WssThread
from api_modules.open_binance_api import OpenBinanceApi
import pytz
tzdata = pytz.timezone('Europe/Moscow') 
from flask import request
import requests


# from flask import Flask, app, redirect, url_for, render_template
from flask_app import app
# ---
class FlaskThread(object): 
    '''docstring for Trader'''
    def __init__(self, ):
        super().__init__()

        self.is_stopped = None
        self._thread = threading.Thread(target=self.thread_function, args=())
        self._lock = threading.Lock()

    def thread_function(self, *args, **kwargs):
        # ====
        app.run(debug=0, host='0.0.0.0', port=5000)        

    def get_data(self, ) -> dict:
        with self._lock:
            pass
    
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
            r = requests.get('http://192.168.1.125:5000/shutdown')
            if r.status_code == 200:
                logging.info(f"[{self.__class__.__name__}] Closed")


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
    w = FlaskThread(

        )
        
    w.start()
    
    # close thread
    # w.close()