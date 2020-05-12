import asyncio
from tls_websockets import TLSWebsocketsServer
from websockets import WebSocketServerProtocol, ConnectionClosedOK


class Application:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.wss_server = TLSWebsocketsServer(
            host="localhost",  # or "0.0.0.0"
            port=5000,
            certfile='certs/svr.chain.pem',
            keyfile='certs/svr.pem',
            cafile='certs/ca.crt.pem',
            loop=self.loop
        )
        self.wss_server.session = self.session
        self.wss_server.run()

    async def session(self, sock: WebSocketServerProtocol, path: str):
        print("new session")
        while True:
            try:
                [buf] = await asyncio.gather(sock.recv(), loop=self.loop, return_exceptions=True)
                if isinstance(buf, Exception):
                    raise buf
                print(len(buf), "byte received")
                with open("output.pcap", "wb") as f:
                    f.write(buf)
                await sock.send("ok")
            except ConnectionClosedOK:
                await sock.close()
                print("session closed")
                break
            except KeyboardInterrupt:
                await sock.close()
                print("exit")


if __name__ == "__main__":
    Application()
