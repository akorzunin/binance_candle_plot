import logging
import sys
import threading
# ---
import pandas as pd
import pickle
import os
from datetime import datetime
from dotenv import load_dotenv
import uvicorn

load_dotenv()
PWD = os.getenv("PWD")
import sys

sys.path.insert(1, f'{PWD}\\modules')
import time
import logging

from thread_module import ThreadModule
from data_API_main import app

# from api_modules.open_binance_api import OpenBinanceApi


# from flask import Flask, app, redirect, url_for, render_template
# ---
class DataApiThread(ThreadModule): 
    '''docstring for Trader'''
    def __init__(self, ):
        super().__init__()

        self.is_stopped = None
        self._thread = threading.Thread(target=self.thread_function, args=())
        self._lock = threading.Lock()

    def thread_function(self, *args, **kwargs):
        # ====
        uvicorn.run(app, debug=1, host="0.0.0.0", port=8000)        

    def get_data(self, ) -> dict:
        with self._lock:
            pass
    
    def start(self):
        '''Start the thread'''
        logging.info(f"[{self.__class__.__name__}] Opening thread")
        self.is_stopped = False
        self._thread.start()

    # def close(self) -> None:
    #     ''' Close the thread'''
    #     # with self._lock:
    #     logging.info(f"[{self.__class__.__name__}] Closing thread")
    #     self.is_stopped = True
    #     exit()
    #         # raise SystemExit
    #         # r = requests.get('http://192.168.1.125:5000/shutdown')
    #         # if r.status_code == 200:
    #         #     logging.info(f"[{self.__class__.__name__}] Closed")


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
    w = DataApiThread(
        )
        
    w.start()
    
    # close thread
    # w.close()