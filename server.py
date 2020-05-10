import socket
import ssl
import os
import asyncio
import websockets
from pathlib import Path


def passwd():
    with open("passwd", "r") as f:
        pswd = f.readline().rstrip(os.linesep)
    return pswd


context = ssl.create_default_context(
    ssl.Purpose.CLIENT_AUTH,
    cafile=Path("certs/ca.crt.pem")
)
context.verify_mode = ssl.CERT_REQUIRED

context.load_cert_chain(
    certfile='certs/svr.chain.pem',
    keyfile='certs/svr.pem',
    password=passwd,
)


async def hello(websocket, path):
    name = await websocket.recv()
    print(f"< {name}")

    greeting = f"Hello {name}!"

    await websocket.send(greeting)
    print(f"> {greeting}")

start_server = websockets.serve(hello, "localhost", 5000, ssl=context)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
