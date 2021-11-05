import asyncio
import json
import os
# from py_html import give_html
import binance_calc
import bs4

MY_IP = ''

def get_json():
    data_dict = {
       'key': str('data'),
    }
    return json.dumps(data_dict)

def run_keepon():
    print('pog')
    # os.startfile(r"C:\Users\akorz\Desktop\skripts\Keep on!.exe")

def run_other():
    print('other')

def get_page():
    a, b = binance_calc.main()
    with open("./file.html") as inf:
        f = inf.read()
    # f = open("./file.html", "r").read()

    soup = bs4.BeautifulSoup(f)
    newRecord = f'<div> som tex, and som useful information: <br> {a=}, <br>{b=} </div>'
    soup.append(bs4.BeautifulSoup(newRecord, 'html.parser'))

    with open("./file.html", "w") as outf:
        outf.write(str(soup))
    return open("./file.html", "r").read() # потом заменить на вызов модуля который обновит данные и пришлет свежие

async def handle_req(reader, writer):
    data = await reader.read(100)
    print(f'{data=}')
    request = data
    if request[:request.find(b' ')] == b'GET':  
        # cut off method
        request = request[request.find(b'/?')+ len(b'/?'):]
        # parse endpoint
        endp = request[:request.find(b' ')]
        if endp == b'run=keepon': run_keepon()
        if endp == b'run=other': run_other()
        if endp == b'state': pass
    addr = writer.get_extra_info('peername')

    print(f"Received {request!r} from {addr!r}")
    # send_data = give_html()
    send_data = ("HTTP/1.1 200 OK\n"
         +"Content-Type: text/html\n"
         +"\n" # Important!
         +str(get_page()))

    # print(f"Send: {send_data.encode()!r}")
    writer.write(send_data.encode())


    await writer.drain()
    print("Close the connection")
    writer.close()

async def main():
    server = await asyncio.start_server(
        handle_req, MY_IP, 8000)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

asyncio.run(main())