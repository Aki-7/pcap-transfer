import ssl
import socket
import os
import asyncio
import websockets
from pathlib import Path

hostname = "localhost"


def passwd():
    with open("passwd", "r") as f:
        pswd = f.readline().rstrip(os.linesep)
    return pswd


context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
context.load_verify_locations(cafile=Path("certs/ca.crt.pem"))

context.load_cert_chain(
    certfile='certs/clt.chain.pem',
    keyfile='certs/clt.pem',
    password=passwd,
)


async def hello():
    uri = "wss://localhost:5000"
    async with websockets.connect(uri, ssl=context) as websocket:
        name = input("What's your name? ")

        await websocket.send(name)
        print(f"> {name}")

        greeting = await websocket.recv()
        print(f"< {greeting}")

asyncio.get_event_loop().run_until_complete(hello())
