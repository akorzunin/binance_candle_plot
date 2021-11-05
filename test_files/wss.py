
import websocket
import _thread
import time
def remove_first_line(filename: str):        
    with open(filename, 'r') as fin:
        data = fin.read().splitlines(True)
    with open(filename, 'w') as fout:
        fout.writelines(data[1:])

def on_message(ws, message):
    FILE_LEN = 1000 - 1
    with open("RVNUSD_data.txt", "a+") as f:
        with open("RVNUSD_data.txt", "r") as fo:
            lines = len([line.strip("\n") for line in fo if line != "\n"])
        rm_lines = lines - FILE_LEN
        for _ in range(rm_lines): remove_first_line("RVNUSD_data.txt")
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
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://stream.binance.com:9443/ws/rvnusdt@ticker",
                            #   on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever()
#     # pog {"e":"24hrTicker","E":1635355176833,"s":"RVNUSDT","p":"-0.01240000","P":"-10.253","w":"0.11187107","x":"0.12101000","c":"0.10854000","Q":"3201.20000000","b":"0.10852000","B":"1690.60000000","a":"0.10858000","A":"2072.50000000","o":"0.12094000","h":"0.12325000","l":"0.09955000","v":"203161498.50000000","q":"22727894.00026700","O":1635268776679,"C":1635355176679,"F":29191179,"L":29280590,"n":89412}
#     {"e":"24hrTicker",
#     "E":1635359410445,
#     "s":"RVNUSDT",
#     "p":"-0.01365000",
#     "P":"-11.238",
#     "w":"0.11147062",
#     "x":"0.12152000",
#     "c":"0.10781000",
#     "Q":"120.00000000",
#     "b":"0.10788000", # верхушка биржевого стакана (на покупку рвн)  value = RVN*a*fee_c; fee_c = 1 - fee*0.01; fee = 0.1
#     "B":"1500.00000000",
#     "a":"0.10795000", # не продажу RVN
#     "A":"1500.00000000",
#     "o":"0.12146000",
#     "h":"0.12325000",
#     "l":"0.09955000",
#     "v":"198283784.20000000",
#     "q":"22102816.04302800",
#     "O":1635273008691,
#     "C":1635359408691,
#     "F":29193833,
#     "L":29282178,
#     "n":88346} 
# #   "e": "24hrTicker",  // Event type
# #   "E": 123456789,     // Event time
# #   "s": "BNBBTC",      // Symbol
# #   "p": "0.0015",      // Price change
# #   "P": "250.00",      // Price change percent
# #   "w": "0.0018",      // Weighted average price
# #   "x": "0.0009",      // First trade(F)-1 price (first trade before the 24hr rolling window)
# #   "c": "0.0025",      // Last price
# #   "Q": "10",          // Last quantity
# #   "b": "0.0024",      // Best bid price
# #   "B": "10",          // Best bid quantity
# #   "a": "0.0026",      // Best ask price
# #   "A": "100",         // Best ask quantity
# #   "o": "0.0010",      // Open price
# #   "h": "0.0025",      // High price
# #   "l": "0.0010",      // Low price
# #   "v": "10000",       // Total traded base asset volume
# #   "q": "18",          // Total traded quote asset volume
# #   "O": 0,             // Statistics open time
# #   "C": 86400000,      // Statistics close time
# #   "F": 0,             // First trade ID
# #   "L": 18150,         // Last trade Id
# #   "n": 18151          // Total number of trades
#     {"e":"24hrTicker","E":1635360448488,"s":"RVNUSDT","p":"-0.01416000","P":"-11.663","w":"0.11138406","x":"0.12140000","c":"0.10725000","Q":"504.50000000","b":"0.10720000","B":"3593.00000000","a":"0.10725000","A":"2543.80000000","o":"0.12141000","h":"0.12325000","l":"0.09955000","v":"198264977.10000000","q":"22083557.60912200","O":1635274048208,"C":1635360448208,"F":29194340,"L":29282594,"n":88255}

# Python 3.9.7 (tags/v3.9.7:1016ef3, Aug 30 2021, 20:19:38) [MSC v.1929 64 bit (AMD64)] on win32
# Type "help", "copyright", "credits" or "license" for more information.
# >>> b = 0.10788000
# >>> amont_RVN = 1
# >>> fee = 0.1
# >>> price = amont_RVN*b*(1+fee*0.01)
# >>> _
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# NameError: name '_' is not defined
# >>> price
# 0.10798788
# >>> b
# 0.10788
# >>> value = amont_RVN*b
# >>> value
# 0.10788
# >>> value*0.999
# 0.10777212
# >>> RVN = 100
# >>> b = 0.10720000
# >>> a = 0.10725000
# >>> USD = RVN*a*(1)
# >>> value = RVN*a
# >>> value
# 10.725
# >>> fee_ = value*fee
# >>> fee
# 0.1
# >>> fee_ = value*fee*0.01
# >>> fee_
# 0.010725
# >>> value - fee_
# 10.714274999999999
# >>> fee_c = 1 - fee*0.01
# >>> fee_c
# 0.999
# >>> value = RVN*a*fee_c
# >>> value
# 10.714274999999999
# >>> value = RVN*a/fee
# >>> value
# 107.24999999999999
# >>> value = RVN*a/(fee*0.01)
# >>> value
# 10725.0
# >>> value = RVN*a/(fee*100)
# >>> value
# 1.0725
# >>> value = RVN*a/(fee*10)
# >>> value
# 10.725
# >>>