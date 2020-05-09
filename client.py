import ssl
import socket
import os
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

conn = context.wrap_socket(
    socket.socket(socket.AF_INET),
    server_hostname=hostname
)

conn.connect((hostname, 5000))

conn.send(b"success!")

conn.close()
