'''collect data from stream binance api to file'''
import websocket
import _thread
import time
def remove_first_line(filename: str):        
    with open(filename, 'r') as fin:
        data = fin.read().splitlines(True)
    with open(filename, 'w') as fout:
        fout.writelines(data[1:])

def on_message(ws, message):
    
    with open(FILE_PATH, "a+") as f:
        with open(FILE_PATH, "r") as fo:
            lines = len([line.strip("\n") for line in fo if line != "\n"])
        if FILE_LEN is not None: 
            rm_lines = lines - (FILE_LEN - 1)
            for _ in range(rm_lines): remove_first_line(FILE_PATH)
        f.write(message+'\n')

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

# def on_open(ws):
#     def run(*args):
#         # for i in range(3):
#         #     time.sleep(1)
#         #     ws.send("Hello %d" % i)
#         # ws.send
#         time.sleep(1)
#         ws.close()
#         print("thread terminating...")
#     _thread.start_new_thread(run, ())

if __name__ == "__main__":
    FILE_PATH = "RVNUSD_data_2.txt"
    FILE_LEN = None # use None to endless test
    VALUT_PAIR = 'rvnusdt' #LOWERCASE!!!
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(f"wss://stream.binance.com:9443/ws/{VALUT_PAIR}@ticker",
                            #   on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever()