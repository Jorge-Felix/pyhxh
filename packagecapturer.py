from scapy.all import *
import argparse
import pandas as pd
from subprocess import call
import socket

parser = argparse.ArgumentParser(description="package capturer")

parser.add_argument("-c", type=int, default=100, help="count of packages to be sniffed")
parser.add_argument("-o", type=str, default='N', help="Creates an output file")
args = parser.parse_args()

COUNT = args.c
OUTPUT = args.o
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.connect(("8.8.8.8",80))
own_ip:str = s.getsockname()[0]
frame = Ether() / IP()

print("[*]INFO[*]")
frame.show()
print("[*]INFO[*]")

packets = sniff(count=COUNT + 1)


def get_protocol_name(proto_num):
    if proto_num == 6:
        return 'TCP'
    elif proto_num == 17:
        return 'UDP'
    else:
        return 'Unknown'



def packets_to_dataframe(packets):
    rows = []
    for packet in packets:
        # Check if the packet has the IPv4 layer
        if packet.haslayer(IP):
            protocol_name = get_protocol_name(packet[IP].proto)

            dest_port = None
            packet_size = None
            packet_data = None

            # Check if the packet has the transport layer (TCP or UDP)
            if packet.haslayer(TCP):
                dest_port = packet[TCP].dport
            elif packet.haslayer(UDP):
                dest_port = packet[UDP].dport

            # Check if the packet has the Raw layer
            if Raw in packet:
                packet_size = len(packet[Raw])
                packet_data = str(packet[Raw].load)

            
            row = {
                'Protocol': protocol_name,
                'Source': packet[IP].src,
                'Destination': packet[IP].dst,
                'Destination Port': dest_port,
                'Packet Size': packet_size,
                'Packet Data': packet_data
            }
            rows.append(row)

        elif packet.haslayer(IPv6):
            protocol_name = get_protocol_name(packet[IPv6].nh)

            dest_port = None
            packet_size = None
            packet_data = None

            if packet.haslayer(TCP):
                dest_port = packet[TCP].dport
            elif packet.haslayer(UDP):
                dest_port = packet[UDP].dport

            # Check if the packet has the Raw layer
            if Raw in packet:
                packet_size = len(packet[Raw])
                packet_data = str(packet[Raw].load)

                

            row = {
                'Protocol': protocol_name,
                'Source': packet[IPv6].src,
                'Destination': packet[IPv6].dst,
                'Destination Port': dest_port,
                'Packet Size': packet_size,
                'Packet Data': bytes(packet_data)
            }
            rows.append(row)

    df = pd.DataFrame(rows).dropna()

    if OUTPUT.lower() == 'y':
        OUTPUT_NAME = input(str("Output file name >> "))
        df.to_csv(f"{OUTPUT_NAME}.csv", index=False)
    elif OUTPUT.lower() == 'n':
        return df
    return df

print(packets_to_dataframe(packets))
