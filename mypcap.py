import dpkt
import pcap
import socket
import datetime
import sys


def mac_addr(address):
    return ':'.join('%02x' % dpkt.compat_ord(b) for b in address)


def inet_to_str(inet):
    try:
        return socket.inet_ntop(socket.AF_INET, inet)
    except ValueError:
        return socket.inet_ntop(socket.AF_INET6, inet)


def printArp(ts: str, arp: dpkt.arp.ARP):
    tpa = inet_to_str(arp.tpa)
    spa = inet_to_str(arp.spa)
    print(
        ts,
        arp.__class__.__name__,
        "who has {tpa:15} tell {sha}".format(
            tpa=tpa,
            sha=spa))


def main(filter):
    sn = pcap.pcap(name=None, promisc=True, immediate=True, timeout_ms=50)
    print("filter:", filter)
    sn.setfilter(filter)

    for ts, pkt in sn:
        eth = dpkt.ethernet.Ethernet(pkt)
        timestamp = str(datetime.datetime.utcfromtimestamp(ts))
        proto = type(eth.data)
        if proto == dpkt.arp.ARP:
            printArp(timestamp, eth.data)
        else:
            print(timestamp, eth.data.__class__.__name__)


if __name__ == "__main__":
    argv = sys.argv
    cmd = argv.pop(0)
    filter = " ".join(argv)
    main(filter)
