import ssl
import socket
import os
import asyncio
import websockets
from pathlib import Path


class TLSWebsocketsClient:
    def __init__(self, uri, certfile, keyfile, cafile,
                 loop=asyncio.get_event_loop()):
        self.uri = uri
        self.__certfile = certfile
        self.__keyfile = keyfile
        self.__cafile = cafile
        self.__ssl_context = self._create_ssl_context()
        self.__lock_until_connected = asyncio.Lock()
        self.__loop = loop
        self.__session_task = None

    def start_session(self):
        self.__loop.run_until_complete(self.__lock_until_connected.acquire())
        self.__session_task = self.__loop.create_task(self.__connect(self.uri))

    def wait_connection(self):
        self.__loop.run_until_complete(self.__lock_until_connected.acquire())

    async def session(self, sock: websockets.WebSocketClientProtocol):
        raise NotImplementedError

    def wait_session_closed(self):
        self.__loop.run_until_complete(self.__session_task)

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

    async def __connect(self, uri):
        async with websockets.connect(uri, ssl=self.__ssl_context) as sock:
            self.__lock_until_connected.release()
            await self.session(sock)


class TLSWebsocketsServer:
    def __init__(
            self,
            certfile,
            keyfile,
            cafile,
            host="localhost",
            port=5000,
            loop=asyncio.get_event_loop()):
        self.host = host
        self.port = port
        self.__certfile = certfile
        self.__keyfile = keyfile
        self.__cafile = cafile
        self.__ssl_context = self._create_ssl_context()
        self.__loop = loop

    def run(self):
        serve = websockets.serve(
            self.session, self.host, self.port, ssl=self.__ssl_context)
        self.__loop.run_until_complete(serve)
        self.__loop.run_forever()

    async def session(self, sock: websockets.WebSocketServerProtocol, path: str):
        raise NotImplementedError

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
