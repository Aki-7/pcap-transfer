import asyncio
import gzip
from tls_websockets import TLSWebsocketsClient
from websockets import WebSocketClientProtocol
from packet_dumper import PacketDumperFromSampleFile


class Application:
    def __init__(self):
        self.__loop = asyncio.get_event_loop()
        self.sock: WebSocketClientProtocol = None
        self.wss_client = TLSWebsocketsClient(
            uri="wss://localhost:5000",
            certfile='certs/clt.chain.pem',
            keyfile='certs/clt.pem',
            cafile='certs/ca.crt.pem',
            loop=self.__loop
        )
        self.wss_client.session = self.session
        self.wss_client.start_session()
        self.wss_client.wait_connection()

        self.packet_dumper = PacketDumperFromSampleFile("input.pcap")
        self.packet_dumper.handle_packet = self.handle_packet
        self.packet_dumper.dump()

        self.wss_client.wait_session_closed()

    def handle_packet(self, packet):
        zipped = gzip.compress(packet)
        self.__loop.run_until_complete(self.sock.send(zipped))

    async def session(self, sock: WebSocketClientProtocol):
        self.sock = sock
        while True:
            try:
                buf = await sock.recv()
                if buf == "ok":
                    break
            except KeyboardInterrupt:
                break


if __name__ == "__main__":
    Application()
