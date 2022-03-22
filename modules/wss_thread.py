import logging
import threading
import time
import websocket
import time
from collections import deque
import ast

class WssThread(object): 
    '''docstring for WssThread'''
    def __init__(self, url: str, maxlen: int=10):
        super(WssThread, self).__init__()
        self.queue = deque(maxlen=maxlen)
        self.url = url
        self.wss_thread = threading.Thread(target=self.thread_function, args=())
        self._lock = threading.Lock()

    def thread_function(self, ):
        def on_open(ws, ):
            logging.info('### Opening wss stream ###')

        def on_message(ws, message):
            self.queue.append(message)

        def on_error(ws, error):
            logging.error(error)
            
        def on_close(ws, close_status_code, close_msg):
            logging.info("### wss stream closed ###")
        # disable massages from wss stream to console
        websocket.enableTrace(False)
        self.ws = websocket.WebSocketApp(
            self.url,
            on_open=on_open,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close
            )
        self.ws.run_forever()
        

    def get_data(self, ) -> dict:
        with self._lock:
            e = (self.queue or [None])[-1]
            try:
                return(ast.literal_eval(e)) 
            except ValueError as err: 
                logging.debug(err)
    
    def start(self):
        '''Start the websocket'''
        self.wss_thread.start()

    def close(self) -> None:
        ''' Close the websocket connection'''
        with self._lock:
            self.ws.keep_running = False

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    w = WssThread(
        url='wss://stream.binance.com:9443/ws/rvnusdt@ticker',
        maxlen=10,
        )
    w.start()

    def foo(wss):
        print(wss.get_data())
    try:
        while True:
            # print(w.get_data())
            foo(w)
            time.sleep(0.1)
    finally:
        # close thread
        w.close()