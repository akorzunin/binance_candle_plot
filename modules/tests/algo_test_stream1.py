import sys
sys.path.insert(1, r'C:\Users\akorz\Documents\binance_bot\binance_candle_plot\modules')
import time
from alg_handler import AlgHandler

# implement this to be able to use it in other modules

# import websocket
# import _thread
# import time
# def remove_first_line(filename: str):        
#     with open(filename, 'r') as fin:
#         data = fin.read().splitlines(True)
#     with open(filename, 'w') as fout:
#         fout.writelines(data[1:])

# def on_message(ws, message):
#     FILE_LEN = 1000 - 1
#     with open("RVNUSD_data.txt", "a+") as f:
#         with open("RVNUSD_data.txt", "r") as fo:
#             lines = len([line.strip("\n") for line in fo if line != "\n"])
#         rm_lines = lines - FILE_LEN
#         for _ in range(rm_lines): remove_first_line("RVNUSD_data.txt")
#         f.write(message+'\n')

# def on_error(ws, error):
#     print(error)

# def on_close(ws, close_status_code, close_msg):
#     print("### closed ###")

# # def on_open(ws):
# #     def run(*args):
# #         # for i in range(3):
# #         #     time.sleep(1)
# #         #     ws.send("Hello %d" % i)
# #         # ws.send
# #         time.sleep(1)
# #         ws.close()
# #         print("thread terminating...")
# #     _thread.start_new_thread(run, ())

# if __name__ == "__main__":
#     websocket.enableTrace(True)
#     ws = websocket.WebSocketApp("wss://stream.binance.com:9443/ws/rvnusdt@ticker",
#                             #   on_open=on_open,
#                               on_message=on_message,
#                               on_error=on_error,
#                               on_close=on_close)

#     ws.run_forever()

#

if __name__ == '__main__':
    alg = AlgHandler(
        # path to txt file
        log_path='./modules/tests/stream_log.txt',
        data_file_path=r"C:\Users\akorz\Documents\binance_bot\binance_candle_plot\RVNUSD_data.txt"
    )
    try:
        # начать чтение потока в файл
        while 1:
            time.sleep(1) # seconds
            alg.calculate()
            alg.evaluate()
    finally:
        pass
        # остановить чтание данных в файл