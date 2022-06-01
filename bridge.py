import threading
import json
import logging
from websocket import create_connection
from websocket_server import WebsocketServer

address: str = '121.40.246.155'
port: str = '27015'
verifykey: str = '1234567890'
miraibotqq: str = '3031718988'
url = 'ws://{}:{}/all?verifyKey={}&qq={}'.format(address, port, verifykey, miraibotqq)

ws = None
sessionkey = ''


def server_onnewclient(client, server):
    server.send_message(client, "Hey client -> " + sessionkey)


def server_onnewmessage(client, server, message):
    server.send_message(client, message)


def doServer():
    server = WebsocketServer(host='127.0.0.1', port=13254, loglevel=logging.INFO)
    server.set_fn_new_client(server_onnewclient)
    server.set_fn_message_received(server_onnewmessage)
    server.run_forever()


def doClient():
    global ws
    global sessionkey
    ws = create_connection(url)
    sessionkey = json.loads(ws.recv())['data']['session']

    while True:
        msg = ws.recv()
        if len(msg) > 0:
            print(msg)


if __name__ == '__main__':
    t1 = threading.Thread(target=doServer)
    t2 = threading.Thread(target=doClient)
    t1.start()
    t2.start()
