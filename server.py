import socket
import ssl
import os
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

socket = socket.socket()
socket.bind(("localhost", 5000))
socket.listen(5)


def deal_with_client(connstream):
    data = connstream.read()
    while data:
        print(data.decode())
        if data == b'success!':
            return True
        data = connstream.read()


while True:
    newsock, addr = socket.accept()
    connstream = context.wrap_socket(newsock, server_side=True)
    try:
        if (deal_with_client(connstream)):
            connstream.close()
            break
    finally:
        connstream.close()
