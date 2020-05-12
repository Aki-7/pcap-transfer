class PacketDumperFromSampleFile:
    def __init__(self, filename: str):
        self.fd = open(filename, "rb")

    def dump(self):
        while True:
            packet = self.fd.readline()
            if packet == b'':
                break
            self.handle_packet(packet)
        self.fd.close()

    def handle_packet(self, packet):
        raise NotImplementedError

    def __del__(self):
        self.fd.close()
