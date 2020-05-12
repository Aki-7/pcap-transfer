import socket
import ssl
import os
import asyncio
import websockets
from pathlib import Path


class TLSWebsocketServer:
    def __init__(self, certfile, keyfile, cafile):
        self.__certfile = certfile
        self.__keyfile = keyfile
        self.__cafile = cafile
        self.__ssl_context = self._create_ssl_context()

    def run(self, host="localhost", port=5000):
        serve = websockets.serve(
            self._session, host, port, ssl=self.__ssl_context)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(serve)
        loop.run_forever()

    async def _session(self, sock: websockets.WebSocketServerProtocol, path: str):
        print("start new session")
        while True:
            try:
                buf = await sock.recv()
                print("receive:", buf)
            except websockets.ConnectionClosedOK:
                await sock.close()
                print("end session")
                break

    def _create_ssl_context(self):
        context = ssl.create_default_context(
            purpose=ssl.Purpose.CLIENT_AUTH,
            cafile=self.__cafile
        )
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_cert_chain(
            certfile=self.__certfile,
            keyfile=self.__keyfile,
            password=self._passwd
        )
        return context

    def _passwd(self):
        with open("passwd", "r") as f:
            pswd = f.readline().rstrip(os.linesep)
        return pswd


if __name__ == "__main__":
    server = TLSWebsocketServer(
        certfile='certs/svr.chain.pem',
        keyfile='certs/svr.pem',
        cafile='certs/ca.crt.pem',
    )
    server.run()
