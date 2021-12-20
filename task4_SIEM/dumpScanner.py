# scapy install https://scapy.readthedocs.io/en/latest/installation.html#current-development-version
from scapy.utils import RawPcapReader
from scapy.layers.l2 import Ether
from scapy.layers.inet import IP, TCP


class NetworkPackage:
    def __init__(self, srcIP, srcPort, dstIP, dstPort):
        self.sourceIP = srcIP
        self.sourcePort = srcPort
        self.destinationIP = dstIP
        self.destinationPort = dstPort

    def __str__(self):
        return "Source " + self.sourceIP + ":" + str(self.sourcePort) \
               + "  Destination " + self.destinationIP + ":" + str(self.destinationPort)


def process_pcap(file_name):
    events = []
    count = 0
    for (pkt_data, pkt_metadata,) in RawPcapReader(file_name):
        # this validation is taken from
        # https://vnetman.github.io/pcap/python/pyshark/scapy/libpcap/2018/10/25/analyzing-packet-captures-with-python-part-1.html
        ether_pkt = Ether(pkt_data)
        if 'type' not in ether_pkt.fields:
            # LLC frames will have 'len' instead of 'type'.
            # We disregard those
            continue

        if ether_pkt.type != 0x0800:
            # disregard non-IPv4 packets
            continue

        ip_pkt = ether_pkt[IP]
        if ip_pkt.proto != 6:
            # Ignore non-TCP packet
            continue

        # add event after validating
        tcp_pkt = ip_pkt[TCP]
        sourceIP = ip_pkt.src
        destinationIP = ip_pkt.dst
        sourcePort = tcp_pkt.sport
        destinationPort = tcp_pkt.dport
        events.append(NetworkPackage(sourceIP, sourcePort, destinationIP, destinationPort))
        count += 1
    print("Packets extracted: ", count)
    return events

