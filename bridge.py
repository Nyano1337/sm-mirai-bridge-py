import asyncio
from websocket import create_connection
from websockets import serve
import json

address: str = '121.40.246.155'
port: str = '27015'
verifykey: str = '1234567890'
miraibotqq: str = '3031718988'
url = 'ws://{}:{}/all?verifyKey={}&qq={}'.format(address, port, verifykey, miraibotqq)


ws = create_connection(url)
sessionkey = json.loads(ws.recv())['data']['session']

async def echo(websocket):
    async for message in websocket:
        ws.send(message)
        fut = asyncio.get_running_loop().run_in_executor(None, ws.recv)
        msg = await asyncio.wrap_future(future=fut)
        print(msg)
        await websocket.send(msg)

async def main():
    async with serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())