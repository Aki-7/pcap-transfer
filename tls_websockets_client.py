import ssl
import socket
import os
import asyncio
import websockets
from pathlib import Path

hostname = "localhost"


class TLSWebsocketClient:
    def __init__(self, certfile, keyfile, cafile):
        self.__certfile = certfile
        self.__keyfile = keyfile
        self.__cafile = cafile
        self.__ssl_context = self._create_ssl_context()
        self.__sock: websockets.WebSocketClientProtocol = None

    def run(self, uri="wss://localhost:5000"):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.__connect(uri))

    async def _session(self, sock: websockets.WebSocketClientProtocol):
        while True:
            try:
                req = input("type something:")
            except KeyboardInterrupt:
                break
            await sock.send(req)

    async def __connect(self, uri):
        async with websockets.connect(uri, ssl=self.__ssl_context) as sock:
            await self._session(sock)

    def _create_ssl_context(self):
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.load_verify_locations(cafile=self.__cafile)
        context.load_cert_chain(
            certfile=self.__certfile,
            keyfile=self.__keyfile,
            password=self._passwd,
        )
        return context

    def _passwd(self):
        with open("passwd", "r") as f:
            pswd = f.readline().rstrip(os.linesep)
        return pswd

    def __del__(self):
        if (self.__sock is None):
            return
        self.__sock.close()


if __name__ == "__main__":
    client = TLSWebsocketClient(
        certfile='certs/clt.chain.pem',
        keyfile='certs/clt.pem',
        cafile='certs/ca.crt.pem'
    )
    client.run()
